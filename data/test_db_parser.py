from db_parser import fix_encoding

def test_quote():
    assert fix_encoding(" &quot;blah&quot; ") == ' "blah" '

def test_ampersand():
    assert fix_encoding(" Hall &amp; Oates ") == ' Hall & Oates '

def test_acdc():
    assert fix_encoding(" AC?DC ") == ' AC/DC '
