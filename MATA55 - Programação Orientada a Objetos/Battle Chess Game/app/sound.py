from .data import paths
from pyglet import media
import random

class SoundPlayer(object):
    """
    Classe para reproduzir sons.
    """
    
    def __init__(self, volume: list[int] = [100, 100], mute: list[bool] = [False, False]):
        self.__effect_player = media.Player()
        self.__music_player = media.Player()
        
        self.set_volume(volume)
        self.set_mute(mute)

        self.__loaded_sounds = {
            "effects": {
                "attacking": self.__load_sounds("effects", "attacking"),
                "defeat": self.__load_sounds("effects", "defeat"),
                "dropping_bishop": self.__load_sounds("effects", "dropping_bishop"),
                "dropping_king": self.__load_sounds("effects", "dropping_king"),
                "dropping_knight": self.__load_sounds("effects", "dropping_knight"),
                "dropping_pawn": self.__load_sounds("effects", "dropping_pawn"),
                "dropping_queen": self.__load_sounds("effects", "dropping_queen"),
                "dropping_rook": self.__load_sounds("effects", "dropping_rook"),
                "getting_bishop": self.__load_sounds("effects", "getting_bishop"),
                "getting_king": self.__load_sounds("effects", "getting_king"),
                "getting_knight": self.__load_sounds("effects", "getting_knight"),
                "getting_pawn": self.__load_sounds("effects", "getting_pawn"),
                "getting_queen": self.__load_sounds("effects", "getting_queen"),
                "getting_rook": self.__load_sounds("effects", "getting_rook"),
                "invalid_movement": self.__load_sounds("effects", "invalid_movement"),
                "movement": self.__load_sounds("effects", "movement"),
                "promotion": self.__load_sounds("effects", "promotion"),
                "starting": self.__load_sounds("effects", "starting"),
                "starting_after_defeat": self.__load_sounds("effects", "starting_after_defeat"),
                "victory": self.__load_sounds("effects", "victory")
            },
            "music": self.__load_sounds("music"),
            "defeat_music": self.__load_sounds("music", "defeat")
        }

        self.__played_musics: list = []
        self.__played_defeat_musics: list = []

    def __load_sounds(self, *path: str) -> list[media.Source]:
        """
        Carrega todos os sons de um determinado diretório.
        """
        sounds = []

        for filename in paths.get_sound_list(*path):
            try: sounds.append(media.load(filename))
            except: print("Failed loading", filename)
        return sounds

    def __play_random_sound(self, sound_list: list[media.Source], music: bool = False):
        """
        Reproduz um som aleatório de uma lista de sons.
        """
        if not sound_list: return

        sound = random.choice(sound_list)
        self.__play_sound(sound, music = music)
        
    def __play_sound(self, sound: media.Source, music: bool = False):
        """
        Reproduz um determinado som.
        """
        self.stop_sound(music = music)
        
        player = self.__music_player if music else self.__effect_player
        
        player.queue(sound)
        player.play()

    def is_muted(self) -> list[bool]:
        """
        Verifica se os reprodutores estão ativados ou não.
        """
        return self.__muted

    def is_playing(self, music = False, all_ = False, any_ = False) -> bool:
        """
        Verifica se algum som está sendo reproduzido.
        """
        if all_: return self.__music_player.playing and self.__effect_player.playing
        if any_: return self.__music_player.playing or self.__effect_player.playing
        return self.__music_player.playing if music else self.__effect_player.playing

    def get_volume(self) -> list[int]:
        """
        Retorna o volume dos reprodutores de efeito e música.
        """
        return self.__volume.copy()

    def play_attacking_sound(self):
        """
        Reproduz som de ataque.
        """
        sounds = self.__loaded_sounds["effects"]["attacking"]
        self.__play_random_sound(sounds)
        
    def play_defeat_music(self):
        """
        Reproduz uma música de derrota.
        """
        if not self.__loaded_sounds["defeat_music"] and not self.__played_defeat_musics: return
        
        # Verifica se todas as músicas já foram reproduzidas. Se sim,
        # todas as músicas ficarão disponíveis novamente.
        if len(self.__loaded_sounds["defeat_music"]) == 0:
            self.__loaded_sounds["defeat_music"] = self.__played_defeat_musics
            self.__played_defeat_musics = []
            
        sound = random.choice(self.__loaded_sounds["defeat_music"])

        # Remove a música temporariamente da lista, para evitar
        # que a mesma seja reproduzida novamente.
        self.__played_defeat_musics.append(sound)
        self.__loaded_sounds["defeat_music"].remove(sound)
        
        self.__play_sound(sound, music = True)

    def play_defeat_sound(self):
        """
        Reproduz som de derrota.
        """
        sounds = self.__loaded_sounds["effects"]["defeat"]
        self.__play_random_sound(sounds)

    def play_dropping_bishop_sound(self):
        """
        Reproduz som de largar o bispo.
        """
        sounds = self.__loaded_sounds["effects"]["dropping_bishop"]
        self.__play_random_sound(sounds)

    def play_dropping_king_sound(self):
        """
        Reproduz som de largar o rei.
        """
        sounds = self.__loaded_sounds["effects"]["dropping_king"]
        self.__play_random_sound(sounds)

    def play_dropping_knight_sound(self):
        """
        Reproduz som de largar o cavalo.
        """
        sounds = self.__loaded_sounds["effects"]["dropping_knight"]
        self.__play_random_sound(sounds)

    def play_dropping_pawn_sound(self):
        """
        Reproduz som de largar o peão.
        """
        sounds = self.__loaded_sounds["effects"]["dropping_pawn"]
        self.__play_random_sound(sounds)

    def play_dropping_queen_sound(self):
        """
        Reproduz som de largar a rainha.
        """
        sounds = self.__loaded_sounds["effects"]["dropping_queen"]
        self.__play_random_sound(sounds)

    def play_dropping_rook_sound(self):
        """
        Reproduz som de largar a torre.
        """
        sounds = self.__loaded_sounds["effects"]["dropping_rook"]
        self.__play_random_sound(sounds)

    def play_getting_bishop_sound(self):
        """
        Reproduz som de selecionar o bispo.
        """
        sounds = self.__loaded_sounds["effects"]["getting_bishop"]
        self.__play_random_sound(sounds)

    def play_getting_king_sound(self):
        """
        Reproduz som de selecionar o rei.
        """
        sounds = self.__loaded_sounds["effects"]["getting_king"]
        self.__play_random_sound(sounds)

    def play_getting_knight_sound(self):
        """
        Reproduz som de selecionar o cavalo.
        """
        sounds = self.__loaded_sounds["effects"]["getting_knight"]
        self.__play_random_sound(sounds)

    def play_getting_pawn_sound(self):
        """
        Reproduz som de selecionar o peão.
        """
        sounds = self.__loaded_sounds["effects"]["getting_pawn"]
        self.__play_random_sound(sounds)

    def play_getting_queen_sound(self):
        """
        Reproduz som de selecionar a rainha.
        """
        sounds = self.__loaded_sounds["effects"]["getting_queen"]
        self.__play_random_sound(sounds)

    def play_getting_rook_sound(self):
        """
        Reproduz som de selecionar a torre.
        """
        sounds = self.__loaded_sounds["effects"]["getting_rook"]
        self.__play_random_sound(sounds)

    def play_invalid_movement_sound(self):
        """
        Reproduz som de movimento inválido.
        """
        sounds = self.__loaded_sounds["effects"]["invalid_movement"]
        self.__play_random_sound(sounds)
        
    def play_movement_sound(self):
        """
        Reproduz som de movimento.
        """
        sounds = self.__loaded_sounds["effects"]["movement"]
        self.__play_random_sound(sounds)

    def play_music(self):
        """
        Reproduz uma música.
        """
        if not self.__loaded_sounds["music"] and not self.__played_musics: return
        
        # Verifica se todas as músicas já foram reproduzidas. Se sim,
        # todas as músicas ficarão disponíveis novamente.
        if len(self.__loaded_sounds["music"]) == 0:
            self.__loaded_sounds["music"] = self.__played_musics
            self.__played_musics = []
            
        sound = random.choice(self.__loaded_sounds["music"])

        # Remove a música temporariamente da lista, para evitar
        # que a mesma seja reproduzida novamente.
        self.__played_musics.append(sound)
        self.__loaded_sounds["music"].remove(sound)
        
        self.__play_sound(sound, music = True)

    def play_promotion_sound(self):
        """
        Reproduz som de promoção.
        """
        sounds = self.__loaded_sounds["effects"]["promotion"]
        self.__play_random_sound(sounds)

    def play_start_sound(self):
        """
        Reproduz som de início de jogo.
        """
        sounds = self.__loaded_sounds["effects"]["starting"]
        self.__play_random_sound(sounds)

    def play_start_after_defeat_sound(self):
        """
        Reproduz som de início de jogo, após uma derrota.
        """
        sounds = self.__loaded_sounds["effects"]["starting_after_defeat"]
        self.__play_random_sound(sounds)
    
    def play_victory_sound(self):
        """
        Reproduz som de vitória.
        """
        sounds = self.__loaded_sounds["effects"]["victory"]
        self.__play_random_sound(sounds)

    def set_mute(self, boolean: list[bool]):
        """
        Ativa ou desativa os reprodutores de efeito e música.
        """
        self.__muted = boolean
        
        if boolean[0]: self.__effect_player.volume = 0
        else: self.__effect_player.volume = self.__volume[0] / 100
        
        if boolean[1]: self.__music_player.volume = 0
        else: self.__music_player.volume = self.__volume[1] / 100
        
    def set_volume(self, value: list[int]):
        """
        Define um volume para os reprodutores de efeito e música.
        """
        self.__volume = value
        
        self.__effect_player.volume = self.__volume[0] / 100
        self.__music_player.volume = self.__volume[1] / 100
        
    def stop_sound(self, music: bool = False, all_: bool = False):
        """
        Interrompe a reprodução de um som.
        """
        while (not music or all_) and self.is_playing(music = False):
            self.__effect_player.next_source()

        while (music or all_) and self.is_playing(music = True):
            self.__music_player.next_source()

