from setuptools import setup, find_packages
setup(
    name="kivy_music_player_package",
    version="0.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_music_player = kivy_music_player.__main__:main'
        ]
    },
    package_data={
        '': ['kivy_music_player_package/*'],
    },
)
