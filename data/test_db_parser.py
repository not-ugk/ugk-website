from db_parser import fix_encoding, fix_id

def test_quote():
    assert fix_encoding(" &quot;blah&quot; ") == ' "blah" '

def test_ampersand():
    assert fix_encoding(" Hall &amp; Oates ") == ' Hall & Oates '

def test_acdc():
    assert fix_encoding(" AC?DC ") == ' AC/DC '

def test_id_fix():
    assert fix_id("bxSW 66ptUg") == 'bxSW_66ptUg'
    assert fix_id(" bxSW66ptUg") == '_bxSW66ptUg'