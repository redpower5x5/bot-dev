from dataclasses import dataclass

@dataclass
class ClubInfo:
    """Информация о клубе
        Attributes
        ----------
        key_name : str
            Название клуба
        description : str
            Описание клуба
        link : str
            Ссылка на чат клуба
        """
    key_name: str
    description: str
    link: str
