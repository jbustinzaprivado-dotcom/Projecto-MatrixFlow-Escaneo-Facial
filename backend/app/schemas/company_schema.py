from pydantic import BaseModel, ConfigDict


class EmpresaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    razon_social: str
    ruc: str
    rubro: str
