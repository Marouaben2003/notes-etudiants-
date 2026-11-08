from auth import register, login, users

def test_register():
    users.clear()
    assert register("amina", "Password123")
    assert not register("amina", "Password123")


def test_login_success():
    users.clear()
    register("amina", "Password123")
    assert login("amina", "Password123")


def test_login_wrong_password():
    users.clear()
    register("amina", "Password123")
    assert not login("amina", "WrongPassword")


def test_login_unknown_user():
    users.clear()
    assert not login("unknown", "Password123")

