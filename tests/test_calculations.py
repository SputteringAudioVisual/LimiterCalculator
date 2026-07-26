"""
Verificación de la cadena de cálculo completa.
Ejecutar desde la raíz del proyecto: python tests/test_calculations.py
"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from src.API.LimiterAPI import LimiterAPI
from Utils.UnitConversor import DBConversor


def run_case(label, amp_power_w, amp_ohm, sensitivity_dbu,
             speaker_power_w, speaker_ohm,
             hpf_hz, protect_pct=0):

    amp = amplifierBase()
    amp.setImpedance(amp_ohm)
    amp.setPower(amp_power_w)
    amp.CalculateRMSPeakValues()
    amp.setDBUSens(sensitivity_dbu)

    spk = speakerBase()
    spk.setImpedance(speaker_ohm)
    spk.setPower(speaker_power_w)
    spk.CalculateRMSPeakValues()

    api = LimiterAPI()
    api.setAmp(amp)
    api.setDriver(spk)
    api.setHPF(hpf_hz)
    api.protect = protect_pct

    api.CalculateRMSLimiter()
    api.calculatePeakLimiter()
    api.calculateTimeParameters()

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Amp:     {amp_power_w}W @ {amp_ohm}Ω  →  V_RMS={amp.V_RMS:.2f}V  Xfactor={amp.Xfactor:.3f}")
    print(f"  Speaker: {speaker_power_w}W @ {speaker_ohm}Ω  →  V_RMS={spk.V_RMS:.2f}V  V_Peak={spk.V_Peak:.2f}V")
    print(f"  HPF: {hpf_hz} Hz   Protection: {protect_pct}%")
    print(f"  --- Results ---")
    print(f"  RMS threshold : {api.RMS_dBuTH:+.2f} dBu  ({api.RMS_VoltageTH:.4f} V)")
    print(f"  Peak threshold: {api.Peak_dBuTH:+.2f} dBu  ({api.Peak_VoltageTH:.4f} V)")
    print(f"  Attack        : {api.attack:.1f} ms")
    print(f"  Release       : {api.release:.1f} ms")

    # --- Manual verification (same formulas, computed inline) ---
    i_rms_amp = math.sqrt(amp_power_w / amp_ohm)
    v_rms_amp = i_rms_amp * amp_ohm
    x = v_rms_amp / DBConversor.DBU2V(sensitivity_dbu)

    i_rms_spk = math.sqrt(speaker_power_w / speaker_ohm)
    v_rms_spk = i_rms_spk * speaker_ohm
    v_peak_spk = v_rms_spk * speakerBase.DutyFactor   # × 2

    rms_th_v  = (v_rms_spk  / x) * (1 - protect_pct / 100)
    peak_th_v = (v_peak_spk / x) * (1 - protect_pct / 200)
    rms_th_dbu  = DBConversor.V2DBU(rms_th_v)
    peak_th_dbu = DBConversor.V2DBU(peak_th_v)
    attack  = 1000 / hpf_hz
    release = 15 * attack

    ok = (
        abs(api.RMS_dBuTH  - rms_th_dbu)  < 1e-9 and
        abs(api.Peak_dBuTH - peak_th_dbu) < 1e-9 and
        abs(api.attack  - attack)  < 1e-9 and
        abs(api.release - release) < 1e-9
    )
    print(f"  Verification  : {'PASS ✓' if ok else 'FAIL ✗'}")
    if not ok:
        print(f"    expected RMS={rms_th_dbu:.6f}  got={api.RMS_dBuTH:.6f}")
        print(f"    expected Peak={peak_th_dbu:.6f}  got={api.Peak_dBuTH:.6f}")
    return ok


if __name__ == '__main__':
    results = []

    # Case 1 – TSA4000 Stereo@4Ω driving PD154
    results.append(run_case(
        label       = "TSA4000 Stereo@4Ω → PD154 (0% protection, HPF=40Hz)",
        amp_power_w = 1123,  amp_ohm = 4, sensitivity_dbu = 2,
        speaker_power_w = 500, speaker_ohm = 8,
        hpf_hz = 40, protect_pct = 0,
    ))

    # Case 2 – same amp, 25% protection, higher HPF
    results.append(run_case(
        label       = "TSA4000 Stereo@4Ω → PD154 (25% protection, HPF=80Hz)",
        amp_power_w = 1123, amp_ohm = 4, sensitivity_dbu = 2,
        speaker_power_w = 500, speaker_ohm = 8,
        hpf_hz = 80, protect_pct = 25,
    ))

    # Case 3 – Bridge@8Ω with low sensitivity amp (1V sens)
    results.append(run_case(
        label       = "TSA4000 Bridge@8Ω → PD154 (0% protection, HPF=100Hz, 1V sens)",
        amp_power_w = 2748, amp_ohm = 8, sensitivity_dbu = DBConversor.V2DBU(1),
        speaker_power_w = 500, speaker_ohm = 8,
        hpf_hz = 100, protect_pct = 0,
    ))

    print(f"\n{'='*60}")
    passed = sum(results)
    print(f"  {passed}/{len(results)} tests passed")
    print(f"{'='*60}\n")
    sys.exit(0 if passed == len(results) else 1)
