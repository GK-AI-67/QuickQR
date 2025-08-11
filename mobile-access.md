# 📱 Mobile Access Guide for QuickQR

## 🌐 Network Access URLs

Your QuickQR application is now accessible from your mobile device using these URLs:

### Frontend (Main Application)
- **URL:** `http://192.168.2.120:5174/`
- **Description:** The main QuickQR web application

### Backend API
- **URL:** `http://192.168.2.120:8000/`
- **API Docs:** `http://192.168.2.120:8000/docs`
- **Health Check:** `http://192.168.2.120:8000/health`

## 📋 Prerequisites

1. **Same WiFi Network:** Make sure your mobile device is connected to the same WiFi network as your computer
2. **Network Discovery:** Your computer's IP address is `192.168.2.120`

## 🔧 How to Access

1. **Open your mobile browser** (Chrome, Safari, etc.)
2. **Navigate to:** `http://192.168.2.120:5174/`
3. **Start generating QR codes** that will be accessible from your mobile device

## 📱 Testing QR Code Scanning

1. **Generate a QR code** using the web application
2. **Scan the QR code** with your mobile device's camera or QR scanner app
3. **The QR code should now work** because it uses the network IP instead of localhost

## 🛠️ Troubleshooting

### If you can't access the application:
1. **Check firewall settings** - Windows Firewall might be blocking connections
2. **Verify WiFi connection** - Both devices must be on the same network
3. **Try different browsers** - Some browsers handle local network connections differently

### To allow Windows Firewall access:
```powershell
# Run this in PowerShell as Administrator
netsh advfirewall firewall add rule name="QuickQR Backend" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="QuickQR Frontend" dir=in action=allow protocol=TCP localport=5174
```

## 🎯 Benefits

- ✅ **QR codes work on mobile** - No more "localhost not found" errors
- ✅ **Cross-device testing** - Test QR codes on actual mobile devices
- ✅ **Real-world scenarios** - Simulate real QR code usage
- ✅ **Network accessibility** - Share with other devices on your network

## 📞 Quick Test

Try generating a QR code with this URL: `http://192.168.2.120:5174/`

This should work perfectly when scanned from your mobile device! 🎉 