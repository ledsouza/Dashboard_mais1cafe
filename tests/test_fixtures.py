def test_mongodb_fixture(mongodb):
    """ This test will pass if uri is set to a valid connection string. """
    assert mongodb.admin.command("ping")["ok"] > 0