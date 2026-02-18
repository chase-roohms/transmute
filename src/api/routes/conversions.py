import json
from fastapi import APIRouter, Path, Request
from converters import ConverterInterface
from registry import ConverterRegistry

router = APIRouter(prefix="/conversions", tags=["conversions"])
regisitry = ConverterRegistry()
UPLOAD_DIR = Path("data/uploads")
CONVERTED_DIR = Path("data/converted")
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/")
def list_conversions():
    return {"conversions": []}

@router.post("/")
async def create_conversion(request: Request):
    body = await request.json()
    id = body.get("id")
    input_format = body.get("input_format")
    output_format = body.get("output_format")
    print(f"Received conversion request: id={id}, input_format={input_format}, output_format={output_format}")
    converter_type = regisitry.get_converter_for_conversion(input_format, output_format)
    if converter_type is None:
        return {"error": f"No converter found for {input_format} to {output_format}"}
    
    converter: ConverterInterface = converter_type(f'{UPLOAD_DIR}/{id}.{input_format}', f'{CONVERTED_DIR}/', input_format, output_format)
    print(converter.convert())
    return {"message": "Conversion created"}