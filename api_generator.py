from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import qrcode
import barcode
from barcode.writer import ImageWriter
import io
# import base64 # Only needed if you plan to return base64 encoded images, not directly used for StreamingResponse

app = FastAPI(
    title="Barcode/QR Code Generator API",
    description="API to generate QR Codes and various types of Barcodes.",
    version="1.0.0"
)

# --- Pydantic Models for Request Bodies ---

class QRCodeRequest(BaseModel):
    data: str = Field(..., example="https://www.example.com", description="The data to encode in the QR Code.")
    filename: str = Field("qrcode.png", example="my_website_qr.png", description="Desired filename (for client-side reference, not saved on server).")
    fill_color: str = Field("black", example="blue", description="Color of the QR code modules (e.g., 'black', 'red', hex codes like '#FF0000').")
    back_color: str = Field("white", example="lightgray", description="Background color of the QR code (e.g., 'white', 'yellow', hex codes).")
    version: int = Field(1, ge=1, le=40, description="The version of the QR code (1-40). Controls size and data capacity.")
    box_size: int = Field(10, ge=1, description="The size of each QR code box/module in pixels.")
    border: int = Field(4, ge=0, description="The thickness of the white border around the QR code.")

class BarcodeRequest(BaseModel):
    barcode_type: str = Field(..., example="ean13", description="The type of barcode (e.g., 'ean8', 'ean13', 'upca', 'code128', 'code39').")
    data: str = Field(..., example="123456789012", description="The data to encode in the barcode. Length and format depend on barcode_type.")
    filename: str = Field("barcode.png", example="product_barcode.png", description="Desired filename (for client-side reference, not saved on server).")
    # Options can be more detailed, but keeping it simple for now
    options: dict = Field({}, example={"text": "Product ID 123", "font_size": 10}, description="Optional customization for barcode (e.g., 'text', 'font_size', 'module_height').")


# --- Helper Functions (adapted from previous generator.py) ---

def _generate_qr_code_image_bytes(data, fill_color, back_color, version, box_size, border):
    """Generates a QR code image into a BytesIO object."""
    try:
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0) # Rewind to the beginning of the stream
        return img_byte_arr
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate QR Code: {e}"
        )

def _generate_barcode_image_bytes(barcode_type, data, options):
    """Generates a barcode image into a BytesIO object."""
    try:
        # Validate barcode type (optional, but good for robust API)
        # You might want a more exhaustive list or dynamic check
        supported_barcode_types = [
            'ean8', 'ean13', 'upca', 'jan', 'isbn10', 'isbn13', 'issn',
            'code39', 'code128', 'pzn', 'gs1' # Added common types
        ]
        if barcode_type not in supported_barcode_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported barcode type: '{barcode_type}'. Supported types: {', '.join(supported_barcode_types)}"
            )

        # The data for some barcode types (like EAN-13) must be a specific length and valid.
        # The library will raise an error if data is invalid, which FastAPI will catch.
        barcode_class = barcode.get(barcode_type, writer=ImageWriter())
        barcode_instance = barcode_class(data)

        img_byte_arr = io.BytesIO()
        barcode_instance.write(img_byte_arr, options=options)
        img_byte_arr.seek(0) # Rewind to the beginning of the stream
        return img_byte_arr
    except barcode.errors.BarcodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data for barcode type '{barcode_type}': {e}. Please check data format and length."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate barcode: {e}"
        )

# --- API Endpoints ---

@app.post("/generate-qr", summary="Generate a QR Code", response_description="The generated QR Code image (PNG format).")
async def generate_qr_code_api(request: QRCodeRequest):
    """
    Generates a QR Code image based on the provided data and parameters.
    The image is returned directly in the response body as a PNG.
    """
    img_bytes = _generate_qr_code_image_bytes(
        request.data,
        request.fill_color,
        request.back_color,
        request.version,
        request.box_size,
        request.border
    )
    return StreamingResponse(img_bytes, media_type="image/png", headers={"Content-Disposition": f"inline; filename=\"{request.filename}\""})

@app.post("/generate-barcode", summary="Generate a Barcode", response_description="The generated Barcode image (PNG format).")
async def generate_barcode_api(request: BarcodeRequest):
    """
    Generates a Barcode image based on the provided data, type, and parameters.
    The image is returned directly in the response body as a PNG.
    """
    img_bytes = _generate_barcode_image_bytes(
        request.barcode_type,
        request.data,
        request.options
    )
    # CORRECTED LINE BELOW: Removed the extra '}"' at the end of the headers dictionary
    return StreamingResponse(img_bytes, media_type="image/png", headers={"Content-Disposition": f"inline; filename=\"{request.filename}\""})

# Optional: Root endpoint for API info
@app.get("/", summary="API Root", response_description="Basic API information.")
async def read_root():
    """
    Provides basic information about the API.
    """
    return JSONResponse(content={
        "message": "Welcome to the Barcode/QR Code Generator API!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "/generate-qr": "POST - Generate a QR Code",
            "/generate-barcode": "POST - Generate a Barcode"
        }
    })