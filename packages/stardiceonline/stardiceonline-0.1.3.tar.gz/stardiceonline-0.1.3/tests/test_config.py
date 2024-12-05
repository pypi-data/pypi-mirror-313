from stardiceonline.tools.config import config

def test_call():
    class args:
        option='show'
    assert len(config(args)) > 0

def _test_switch_sim():
    class args:
        option='simulation_mode'
    result = config(args)
    args.option='real_mode'
    result2 = config(args)
    assert result2.startswith("Back")
    
