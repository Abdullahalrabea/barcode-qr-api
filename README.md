![Subtitle(1)](https://github.com/user-attachments/assets/cf1b8b37-7824-4501-87e0-8168340201b3)
# Barcode & QR Code Generator API

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.x-009688?style=for-the-badge&logo=fastapi)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.x-orange?style=for-the-badge&logo=uvicorn)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A powerful and easy-to-use API for generating high-quality QR Codes and various types of Barcodes. Built with FastAPI, this service is designed for seamless integration into any application requiring on-demand image generation for data encoding.

## ✨ Features

* **QR Code Generation:** Create QR codes from any text or URL with customizable colors, size (version), box size, and border.
* **Diverse Barcode Support:** Generate common barcode types including EAN-8, EAN-13, UPC-A, Code 39, Code 128, ISBN-10, ISBN-13, and more.
* **Image Output:** All generated codes are returned as high-quality PNG image files.
* **Fast & Reliable:** Leverages the performance of FastAPI and battle-tested Python libraries.
* **Developer-Friendly:** Clear API endpoints with automatic interactive documentation (Swagger UI).

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.8+ 
* pip (Python package installer) 
* Git
* Visual Studio Code (recommended IDE)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```
    *(Remember to replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME`)*

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the API Locally

1.  **Ensure your virtual environment is active.**
2.  **Start the Uvicorn server:**
    ```bash
    uvicorn api_generator:app --reload
    ```
    The API will be accessible at `http://127.0.0.1:8000`.

### API Documentation

Once the API is running, you can access the interactive Swagger UI documentation at:
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

This documentation allows you to test the endpoints directly from your browser.

## ⚙️ API Endpoints

### 1. Generate QR Code (`POST /generate-qr`)

Generates a QR code image.

* **Request Body (JSON):**
    ```json
    {
      "data": "Your content here (e.g., URL, text)",
      "filename": "my_qr_code.png",
      "fill_color": "black",
      "back_color": "white",
      "version": 1,
      "box_size": 10,
      "border": 4
    }
    ```
* **Response:** `image/png` (binary image data)

### 2. Generate Barcode (`POST /generate-barcode`)

Generates a barcode image of a specified type.

* **Request Body (JSON):**
    ```json
    {
      "barcode_type": "ean13",
      "data": "123456789012",
      "filename": "my_barcode.png",
      "options": {
        "text": "Product ID",
        "font_size": 10
      }
    }
    ```
    *Supported `barcode_type` values include: `ean8`, `ean13`, `upca`, `code39`, `code128`, `isbn10`, `isbn13`, `issn`, `pzn`, `gs1`.*
* **Response:** `image/png` (binary image data)

## 🤝 Contributing

Contributions are welcome! If you have suggestions or find issues, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
