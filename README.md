# QuickQR - AI-Powered QR Code Generator

A modern, AI-enhanced QR code generator application with a beautiful user interface.

## 🚀 Features

- **AI-Powered QR Generation**: Smart suggestions and content optimization
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Multiple QR Types**: URL, text, contact info, WiFi, and more
- **Customization**: Colors, logos, and styling options
- **Real-time Preview**: Instant QR code generation and preview
- **Export Options**: PNG, SVG, and PDF formats
- **PDF Designer**: Create printable, branded PDFs with logo, header, footer, and AI-assisted sections
- **User-Friendly**: Intuitive interface for all users
- **Database Storage**: All designs and content stored securely
- **Analytics**: Track QR code usage and scans
- **Search & Management**: Find and manage your QR designs

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for fast development
- **React Router** for navigation
- **Lucide React** for icons
- **React Hook Form** for form handling

### Backend
- **Python FastAPI** for API
- **Pydantic** for data validation
- **SQLAlchemy** with SQLite database
- **QR Code generation** with qrcode library
- **AI Integration** for smart suggestions
- **CORS** enabled for frontend communication
- **File upload** and storage management

## 📁 Project Structure

```
QuickQR/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── backend/                # FastAPI backend application
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Core configurations
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── requirements.txt    # Python dependencies
│   ├── init_db.py         # Database initialization
│   ├── quickqr.db         # SQLite database (created on first run)
│   ├── uploads/           # Uploaded files directory
│   └── main.py           # FastAPI application entry
├── docs/                  # Documentation
└── README.md             # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Initialize the database
python init_db.py

# Start the application
python main.py
# Or use uvicorn directly
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### PDF Designer (New)
- Navigate to `http://localhost:5173/pdf-designer` (also available from the header as "PDF Designer")
- Upload or paste a logo URL, set header and footer
- Add text boxes; for each, type a prompt and click "Generate with AI" to fill content
- Click "View PDF" to preview in a new tab or "Download PDF" to save

Under the hood, the page renders an A4 preview and uses `html2canvas` + `jsPDF` to produce a PDF. AI content uses the existing `/ai/generate-content` backend endpoint.

## 🗄️ Database Management

The application uses SQLite for storing user designs and content. For detailed database setup and management instructions, see [DATABASE.md](backend/DATABASE.md).

### Quick Database Commands
```bash
# Initialize database (first time setup)
python init_db.py

# Reset database (clear all data)
python init_db.py reset

# Backup database
cp quickqr.db quickqr_backup_$(date +%Y%m%d_%H%M%S).db
```

## 🎨 Features Overview

### QR Code Types Supported
- **URL QR Codes**: Direct links to websites
- **Text QR Codes**: Plain text content
- **Contact QR Codes**: vCard format contact information
- **WiFi QR Codes**: Network credentials
- **Email QR Codes**: Pre-filled email composition
- **Phone QR Codes**: Direct phone number dialing
- **SMS QR Codes**: Pre-filled text messages

### AI Features
- **Smart Content Suggestions**: AI-powered content recommendations
- **URL Optimization**: Intelligent URL shortening and validation
- **Content Analysis**: AI analysis of QR code content
- **AI PDF Sections**: Use prompts to generate section content in the new PDF Designer
- **Usage Analytics**: Smart insights on QR code usage

### Customization Options
- **Color Schemes**: Custom foreground and background colors
- **Logo Integration**: Add company logos to QR codes
- **Style Variations**: Different QR code styles
- **Size Options**: Multiple size configurations
- **Error Correction**: Adjustable error correction levels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

�� Access Points:
Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs
🛠️ Tech Stack:
Frontend: React 18, TypeScript, Tailwind CSS, Vite, Framer Motion
Backend: Python FastAPI, Pydantic, QR Code library, OpenAI API
Development: Hot reload, TypeScript, ESLint, Prettier
The application is now ready to use! It includes everything you requested:
✅ Latest frontend technologies (React 18, TypeScript, Tailwind CSS)
✅ Python FastAPI backend with AI integration
✅ User-friendly modern UI
✅ AI-powered QR code generation
✅ Proper project structure and documentation
Ganapati Bappa Moriya! 🐘🙏 Your QuickQR application is now complete and ready to generate beautiful QR codes with AI intelligence!

**Ganapati Bappa Moriya!** 🐘🙏 

## Lost & Found QR Flow

This feature lets you generate a QR that on first scan asks for details, locks them, and on subsequent scans shows read‑only info – all via the same URL.

- Frontend routes
  - Public scan page: `/lost-and-found/:qrId` → renders `src/pages/ContactQRPage.tsx`
  - Generator UI: `/contact-qr` (authenticated)

- Backend endpoints
  - POST `/api/v1/lost-and-found/generate` → returns `qr_id`, `view_url`
  - GET `/api/v1/lost-and-found/{qr_id}` → returns
    - `is_first_scan`: true when no permissions exist yet (first time)
    - `details`: filtered by permissions on subsequent scans
  - POST `/api/v1/lost-and-found/update-details` → body includes details plus optional `permissions` and `lock`

- First scan (edit)
  - Open the QR URL: `https://<frontend>/lost-and-found/<qrId>`
  - Backend returns `is_first_scan: true` (no permissions yet)
  - `ContactQRPage` shows a form (first_name, last_name, phone_number, address, address_location) with visibility toggles
  - On Save, frontend calls `update-details` with:
    - details fields
    - `permissions`: `{ field: 'visible' | 'hidden' }`
    - `lock: true`
  - Backend stores permissions in `qr_permission_dtls` and blocks further edits

- Subsequent scans (view)
  - Same URL returns read‑only `details` filtered by stored permissions
  - Optional query parameters `?user_id=<id>&lat=..&lng=..` are supported; scan events record IP/UA/location

- Data model notes
  - `lost_and_found_qr.qr_url` stores the public view URL
  - `qr_permission_dtls` stores per‑field permissions

- Configuration
  - Backend builds `view_url` using `FRONTEND_BASE_URL` (fallbacks: production → Render URL, dev → `http://localhost:5173`)
  - Admin user ID (for privileged edit in some flows): `1c0aa08c-aae9-4634-9e88-3e0a5605bb99`
