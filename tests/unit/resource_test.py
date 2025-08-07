def test_resource():
    from importlib.resources import files

    resource_dir = files("zero.resources")
    assert resource_dir.is_dir()

    sprites_dir = resource_dir.joinpath("sprites")
    assert sprites_dir.is_dir()

    potato_sprite = sprites_dir.joinpath("potato.png")
    assert potato_sprite.is_file()

    audio_dir = resource_dir.joinpath("audio")
    assert audio_dir.is_dir()

    clank_sound = audio_dir.joinpath("clank.wav")
    assert clank_sound.is_file()
