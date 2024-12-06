from thesis.services.files.config import ThesisFileServiceConfig

def test_allowed_types():
    assert getattr(ThesisFileServiceConfig, 'allowed_mimetypes', None) is not None
    assert getattr(ThesisFileServiceConfig, 'allowed_extensions', None) is not None