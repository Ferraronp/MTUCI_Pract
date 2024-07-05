from pydantic import BaseModel
from enum import Enum

import sqlalchemy
from db_session import SqlAlchemyBase


class VacancyParser(BaseModel):
    title: str
    experience: str
    work_hours: str
    salary: str
    company: str
    address: str
    metro: str
    vacancy_url: str


class PartTimeVal(Enum):
    VAL1 = 'from_four_to_six_hours_in_a_day'  # от 4 часов в день
    VAL2 = 'employment_part'  # неполный день
    VAL3 = 'start_after_sixteen'  # по вечерам
    VAL4 = 'only_saturday_and_sunday'  # по выходным
    VAL5 = 'employment_project'  # разовое задание
    VAL6 = ''


class EducationVal(Enum):
    VAL1 = 'not_required_or_not_specified'  # не указано, не имеет значения
    VAL2 = 'higher'  # высшее
    VAL3 = 'special_secondary'  # Среднее профессиональное
    VAL4 = ''


class ExperienceVal(Enum):
    VAL1 = 'between1And3'  # от 1 года до 3 лет
    VAL2 = 'noExperience'  # нет опыта
    VAL3 = 'between3And6'  # от 3 до 6 лет
    VAL4 = 'moreThan6'  # больше 6 лет
    VAL5 = ''


class EmploymentVal(Enum):
    VAL1 = 'full'  # Полная занятость
    VAL2 = 'part'  # Частичная
    VAL3 = 'probation'  # Стажировка
    VAL4 = 'project'  # Проектная работа
    VAL5 = 'volunteer'  # Волонтёрство
    VAL6 = ''


class ScheduleVal(Enum):
    VAL1 = 'fullDay'  # Полный рабочий день
    VAL2 = 'shift'  # Сменный график
    VAL3 = 'flyInFlyOut'  # Вахтовый метод
    VAL4 = 'remote'  # Удалённая работа
    VAL5 = 'flexible'  # Гибкий график
    VAL6 = ''


class LabelVal(Enum):
    VAL1 = 'not_from_agency'  # Без вакансий от кадровых агентств
    VAL2 = 'with_address'  # С адресом
    VAL3 = 'low_performance'  # Меньше 10 откликов
    VAL4 = 'accept_handicapped'  # Доступные людям с инвалидностью
    VAL5 = 'accredited_it'  # От аккредитованных ИТ-компаний
    VAL6 = 'accept_kids'  # Доступные с 14 лет
    VAL7 = ''


class VacancyAPIParams(BaseModel):
    text: str = ''
    part_time: PartTimeVal | list[PartTimeVal] = ''
    salary: int = 0  # Зарплата от ...
    only_with_salary: bool = False  # Указан доход
    education: EducationVal | list[EducationVal] = ''
    experience: ExperienceVal = ''
    employment: EmploymentVal | list[EmploymentVal] = ''
    accept_temporary: bool = False  # Оформление по ГПХ или по совместительству
    schedule: ScheduleVal | list[ScheduleVal] = ''
    label: LabelVal | list[LabelVal] = ''  # Другие параметры


class VacancyDatabaseModel(SqlAlchemyBase):
    __tablename__ = 'vacancy'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    experience = sqlalchemy.Column(sqlalchemy.String)
    work_hours = sqlalchemy.Column(sqlalchemy.String)
    salary = sqlalchemy.Column(sqlalchemy.String)
    company = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    metro = sqlalchemy.Column(sqlalchemy.String)
    vacancy_url = sqlalchemy.Column(sqlalchemy.String)
