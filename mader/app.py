from fastapi import FastAPI

from mader.schemas import ReadRoot

app = FastAPI()


@app.get('/', response_model=ReadRoot)
def read_root():
    return {'message': 'Meu Acervo Digital de Romances'}
