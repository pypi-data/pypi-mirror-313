from ....client.credentials import CredentialsApi


def test_default_site_id():
    creds = CredentialsApi(  # noqa: S106
        server_url="url",
        user="test_user",
        password="test_pwd",
        token="token",
        token_name="token_name",
        site_id=None,
    )
    assert creds.to_dict()["site_id"] == ""
