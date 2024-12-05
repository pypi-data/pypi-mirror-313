import json

import pytest
from functools import partial
from las.credentials import (
    Credentials,
    MissingCredentials,
    NULL_TOKEN,
    read_from_environ,
    read_from_file,
    read_token_from_cache,
    write_token_to_cache,
    guess_credentials,
)


@pytest.fixture
def section():
    return 'test'


@pytest.fixture
def credentials_path(tmp_path, section):
    credentials_path = tmp_path / 'credentials.cfg'
    credentials_path.write_text('\n'.join([
        f'[{section}]',
        'client_id = test',
        'auth_endpoint = test',
        'api_endpoint = test',
        'client_secret = test',
    ]))
    return credentials_path


@pytest.fixture(scope='function')
def cache_path(tmp_path):
    return tmp_path / 'token-cache.json'


def mock_read_from_environ(*args, **kwargs):
    return ['foo', 'bar', 'baz', 'foobar']

def equal_credentials(c0, c1):
    return all([
        c0.client_id == c1.client_id,
        c0.client_secret == c1.client_secret,
        c0.auth_endpoint == c1.auth_endpoint,
        c0.api_endpoint == c1.api_endpoint,
    ])

@pytest.mark.parametrize('section', ['default'])
def test_guess_credentials(section, credentials_path):
    credentials_from_env = Credentials(*mock_read_from_environ())

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr('las.credentials.read_from_environ', mock_read_from_environ)
        mp.setattr('las.credentials.read_from_file', partial(read_from_file, credentials_path=credentials_path))

        # Default to using credentials defined in the environment
        assert equal_credentials(credentials_from_env, guess_credentials())

        # Use credentials defined in the config if a profile is specified
        credentials_from_file = guess_credentials(profile=section)
        assert not equal_credentials(credentials_from_env, credentials_from_file)

        # Although credentials are defined in the environment we will not use these when a profile is provided
        with pytest.raises(MissingCredentials):
            guess_credentials(profile='missing-section')

        # Use credentials from file if the credentials from the environment are incomplete
        mp.setattr('las.credentials.read_from_environ', lambda: mock_read_from_environ()[:2])
        equal_credentials(guess_credentials(), credentials_from_file)


def test_read_token_from_cache(cache_path, token, section):
    cache = {section: token}
    cache_path.write_text(json.dumps(cache))
    cached_token = read_token_from_cache(section, cache_path)
    assert token['access_token'], token['expires_in'] == cached_token


def test_write_token_to_cache(cache_path, token, section):
    write_token_to_cache(section, (token['access_token'], token['expires_in']), cache_path)
    cache = json.loads(cache_path.read_text())
    assert token == cache[section]


def test_credentials_with_empty_cache(client):
    assert client.credentials._token == NULL_TOKEN
    assert client.credentials.cached_profile is None


def test_credentials_with_cache(cache_path, token, section):
    write_token_to_cache(section, (token['access_token'], token['expires_in']), cache_path)
    credentials = Credentials(*read_from_environ(), cached_profile=section, cache_path=cache_path)
    assert credentials._token == (token['access_token'], token['expires_in'])
    assert credentials.cached_profile == section


def test_read_from_file_with_cache(credentials_path, section, token, cache_path):
    write_token_to_cache(section, (token['access_token'], token['expires_in']), cache_path)
    credentials_path.write_text(credentials_path.read_text() + '\nuse_cache = true')
    args = read_from_file(str(credentials_path), section)

    credentials = Credentials(*args, cache_path=cache_path)
    assert credentials.cached_profile == section
    assert credentials._token == (token['access_token'], token['expires_in'])


def test_read_from_file_with_no_cache(credentials_path, section, token, cache_path):
    write_token_to_cache(section, (token['access_token'], token['expires_in']), cache_path)
    credentials_path.write_text(credentials_path.read_text() + '\nuse_cache = false')
    args = read_from_file(str(credentials_path), section)

    credentials = Credentials(*args, cache_path=cache_path)
    assert credentials.cached_profile is None
    assert credentials._token == NULL_TOKEN


def test_read_from_file_without_cache(credentials_path, section, token, cache_path):
    write_token_to_cache(section, (token['access_token'], token['expires_in']), cache_path)
    args = read_from_file(str(credentials_path), section)

    credentials = Credentials(*args, cache_path=cache_path)
    assert credentials.cached_profile is None
    assert credentials._token == NULL_TOKEN
