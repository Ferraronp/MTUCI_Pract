from fastapi import FastAPI
from vacancy_model import VacancyAPIParams, VacancyParser, VacancyDatabaseModel
from main import get_vacancy_list
from fastapi.responses import HTMLResponse

import db_session

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column

metadata = MetaData()
engine = create_engine('postgresql+psycopg2://postgres:1234@db/dbname')
vacancy = Table('vacancy', metadata,
                Column('id', Integer(), primary_key=True),
                Column('title', String()),
                Column('experience', String()),
                Column('work_hours', String()),
                Column('salary', String()),
                Column('company', String()),
                Column('address', String()),
                Column('metro', String()),
                Column('vacancy_url', String())
                )
metadata.create_all(engine)
db_session.global_init("postgres:1234@db/dbname")
app = FastAPI()


@app.post("/")
def update_db(params: VacancyAPIParams):
    db_sess = db_session.create_session()
    db_sess.query(VacancyDatabaseModel).delete()
    db_sess.commit()
    db_sess.close()

    f = get_vacancy_list(**params.__dict__)
    for i in f:
        db_sess = db_session.create_session()
        vacancy = VacancyDatabaseModel(**i.__dict__)
        db_sess.add(vacancy)
        db_sess.commit()
        db_sess.close()


@app.get("/hello", response_model=list[VacancyParser])
@app.post("/hello", response_model=list[VacancyParser])
def hello():
    db_sess = db_session.create_session()
    f = db_sess.query(VacancyDatabaseModel).all()
    return f


@app.get("/items/")
def read_items():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
    
    <p><b>Профессия, должность или вакансия:</b></p>
    <p><input id="text" name="text"></p>
    
    <p><b>Подработка:</b></p>
    <p><input name="parttime" type="checkbox" value="from_four_to_six_hours_in_a_day"> от 4 часов в день</p>
    <p><input name="parttime" type="checkbox" value="employment_part"> неполный день</p>
    <p><input name="parttime" type="checkbox" value="start_after_sixteen"> по вечерам</p>
    <p><input name="parttime" type="checkbox" value="only_saturday_and_sunday"> по выходным</p>
    <p><input name="parttime" type="checkbox" value="employment_project"> разовое задание</p>
    
    <p><b>Уровень дохода:</b></p>
    <p>Уровень дохода от: <input id="salary" name="salary"></p>
    <p><input name="only_with_salary" type="checkbox" value="only_with_salary"> Указан доход</p>
    
    <p><b>Образование:</b></p>
    <p><input name="education" type="checkbox" value="not_required_or_not_specified"> Не указано, не имеет значения</p>
    <p><input name="education" type="checkbox" value="higher"> Высшее</p>
    <p><input name="education" type="checkbox" value="special_secondary"> Среднее профессиональное</p>
    
    <p><b>Опыт работы:</b></p>
    <p><input name="experience" type="radio" value="between1And3"> от 1 года до 3 лет</p>
    <p><input name="experience" type="radio" value="noExperience"> нет опыта</p>
    <p><input name="experience" type="radio" value="between3And6"> от 3 до 6 лет</p>
    <p><input name="experience" type="radio" value="moreThan6"> больше 6 лет</p>
    <p><input name="experience" type="radio" value="" checked> не имеет значения</p>
    
    <p><b>Тип занятости:</b></p>
    <p><input name="employment" type="checkbox" value="full"> Полная занятость</p>
    <p><input name="employment" type="checkbox" value="part"> Частичная</p>
    <p><input name="employment" type="checkbox" value="probation"> Стажировка</p>
    <p><input name="employment" type="checkbox" value="project"> Проектная работа</p>
    <p><input name="employment" type="checkbox" value="volunteer"> Волонтёрство</p>
    
    <p><b>Оформление по ГПХ или по совместительству:</b></p>
    <p><input name="accept_temporary" type="checkbox" value="accept_temporary"> Оформление по ГПХ или по совместительству</p>
        
    <p><b>График работы:</b></p>
    <p><input name="schedule" type="checkbox" value="fullDay"> Полный рабочий день</p>
    <p><input name="schedule" type="checkbox" value="shift"> Сменный график</p>
    <p><input name="schedule" type="checkbox" value="flyInFlyOut"> Вахтовый метод</p>
    <p><input name="schedule" type="checkbox" value="remote"> Удалённая работа</p>
    <p><input name="schedule" type="checkbox" value="flexible"> Гибкий график</p>
    
    <p><b>Другие параметры:</b></p>
    <p><input name="label" type="checkbox" value="not_from_agency"> Без вакансий от кадровых агентств</p>
    <p><input name="label" type="checkbox" value="with_address"> С адресом</p>
    <p><input name="label" type="checkbox" value="low_performance"> Меньше 10 откликов</p>
    <p><input name="label" type="checkbox" value="accept_handicapped"> Доступные людям с инвалидностью</p>
    <p><input name="label" type="checkbox" value="accredited_it"> От аккредитованных ИТ-компаний</p>
    <p><input name="label" type="checkbox" value="accept_kids"> Доступные с 14 лет</p>
        
        <button onclick="send()">Отправить</button>
    <script>
        async function send(){
            const text = document.getElementById("text").value;
        
            var checkboxes = document.getElementsByName('parttime');
              var part_time = [""];
              for (var index = 0; index < checkboxes.length; index++) {
                 if (checkboxes[index].checked) {
                    part_time.push(checkboxes[index].value);
                 }
              }
     
            const salary = Number(document.getElementById("salary").value);
            
            var checkboxes = document.getElementsByName('only_with_salary');
            var only_with_salary = checkboxes[0].checked;
            
            var checkboxes = document.getElementsByName('education');
              var education = [];
              for (var index = 0; index < checkboxes.length; index++) {
                 if (checkboxes[index].checked) {
                    education.push(checkboxes[index].value);
                 }
              }
            
            const experience = document.querySelector('input[name="experience"]:checked').value;
            
            var checkboxes = document.getElementsByName('employment');
              var employment = [];
              for (var index = 0; index < checkboxes.length; index++) {
                 if (checkboxes[index].checked) {
                    employment.push(checkboxes[index].value);
                 }
              }
              
              
            var checkboxes = document.getElementsByName('accept_temporary');
            var accept_temporary = checkboxes[0].checked;
            
            var checkboxes = document.getElementsByName('schedule');
              var schedule = [];
              for (var index = 0; index < checkboxes.length; index++) {
                 if (checkboxes[index].checked) {
                    schedule.push(checkboxes[index].value);
                 }
              }
              
            var checkboxes = document.getElementsByName('label');
              var label = [];
              for (var index = 0; index < checkboxes.length; index++) {
                 if (checkboxes[index].checked) {
                    label.push(checkboxes[index].value);
                 }
              }
     
            
            const response = await fetch("/", {
                    method: "POST",
                    headers: { "Accept": "application/json", "Content-Type": "application/json" },
                    body: JSON.stringify({ 
                        text: text,
                        part_time: part_time,
                        salary: salary,
                        only_with_salary: only_with_salary,
                        education: education,
                        experience: experience,
                        employment: employment,
                        accept_temporary: accept_temporary,
                        schedule: schedule,
                        label: label
                    })
                });
                if (response.ok) {
                    const data = await response.json();
                    window.location.href = '/hello';
                }
                else
                    console.log(response);
        }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
