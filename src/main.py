from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import sqlite3
import hashlib
import jwt
import datetime
import json
import os
import base64
from functools import wraps
from enhanced_ai_captions_simple import EnhancedAICaptionGenerator

app = Flask(__name__)
app.secret_key = 'restaurant-social-mobile-secret-key-2024'

# Initialize Enhanced AI Caption Generator
openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
ai_caption_generator = EnhancedAICaptionGenerator(openai_api_key)

# Database initialization
def init_db():
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Restaurants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            cuisine TEXT,
            location TEXT,
            phone TEXT,
            website TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Social accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS social_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            platform TEXT,
            account_id TEXT,
            access_token TEXT,
            refresh_token TEXT,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')
    
    # Posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            content TEXT,
            media_urls TEXT,
            platforms TEXT,
            scheduled_time TIMESTAMP,
            status TEXT DEFAULT 'draft',
            engagement_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')
    
    # Mobile sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mobile_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            device_id TEXT,
            push_token TEXT,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Mobile PWA Template
MOBILE_APP_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Restaurant Social - Mobile App</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#6366f1">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Restaurant Social">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%236366f1'/><text y='50' x='50' text-anchor='middle' dy='0.35em' font-size='50' fill='white'>🍽️</text></svg>">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }
        
        .mobile-container {
            max-width: 100%;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            position: relative;
        }
        
        .mobile-header {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: env(safe-area-inset-top, 20px) 20px 20px 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .app-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .user-info {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .mobile-content {
            padding: 20px;
            padding-bottom: 100px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card:active {
            transform: scale(0.95);
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
        }
        
        .feature-icon {
            font-size: 32px;
            margin-bottom: 10px;
            display: block;
        }
        
        .feature-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        
        .feature-desc {
            font-size: 12px;
            color: #666;
            line-height: 1.4;
        }
        
        .quick-actions {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        
        .action-button {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .action-button:active {
            transform: scale(0.98);
        }
        
        .action-button.secondary {
            background: linear-gradient(135deg, #10b981, #059669);
        }
        
        .action-button.camera {
            background: linear-gradient(135deg, #f59e0b, #d97706);
        }
        
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            border-top: 1px solid #e5e7eb;
            padding: env(safe-area-inset-bottom, 10px) 10px 10px 10px;
            display: flex;
            justify-content: space-around;
            z-index: 100;
        }
        
        .nav-item {
            flex: 1;
            text-align: center;
            padding: 8px;
            color: #6b7280;
            text-decoration: none;
            font-size: 12px;
            transition: color 0.3s ease;
        }
        
        .nav-item.active {
            color: #6366f1;
        }
        
        .nav-icon {
            font-size: 20px;
            display: block;
            margin-bottom: 4px;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            padding: 20px;
        }
        
        .modal-content {
            background: white;
            border-radius: 16px;
            padding: 20px;
            max-height: 80vh;
            overflow-y: auto;
            margin-top: 10vh;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .modal-title {
            font-size: 20px;
            font-weight: 600;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #6b7280;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #6366f1;
        }
        
        .form-textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 16px;
            min-height: 100px;
            resize: vertical;
            font-family: inherit;
        }
        
        .camera-container {
            position: relative;
            margin-bottom: 20px;
        }
        
        .camera-preview {
            width: 100%;
            height: 200px;
            background: #f3f4f6;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #6b7280;
            border: 2px dashed #d1d5db;
        }
        
        .camera-input {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }
        
        .platform-selector {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .platform-option {
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: white;
        }
        
        .platform-option.selected {
            border-color: #6366f1;
            background: #f0f9ff;
            color: #6366f1;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            left: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 16px;
            border-radius: 8px;
            z-index: 2000;
            transform: translateY(-100px);
            transition: transform 0.3s ease;
        }
        
        .notification.show {
            transform: translateY(0);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #6366f1;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 12px;
            color: #6b7280;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #6b7280;
        }
        
        .spinner {
            width: 32px;
            height: 32px;
            border: 3px solid #e5e7eb;
            border-top: 3px solid #6366f1;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .offline-indicator {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ef4444;
            color: white;
            text-align: center;
            padding: 8px;
            font-size: 14px;
            z-index: 1001;
            transform: translateY(-100%);
            transition: transform 0.3s ease;
        }
        
        .offline-indicator.show {
            transform: translateY(0);
        }
        
        @media (max-width: 480px) {
            .mobile-content {
                padding: 15px;
            }
            
            .feature-grid {
                gap: 12px;
            }
            
            .feature-card {
                padding: 16px;
            }
            
            .feature-icon {
                font-size: 28px;
            }
        }
    </style>
</head>
<body>
    <div class="mobile-container">
        <div class="offline-indicator" id="offlineIndicator">
            📶 You're offline. Changes will sync when connected.
        </div>
        
        <div class="mobile-header">
            <div class="app-title">🍽️ Restaurant Social</div>
            <div class="user-info" id="userInfo">Loading...</div>
        </div>
        
        <div class="mobile-content">
            <div class="quick-actions">
                <div class="section-title">📱 Quick Actions</div>
                <button class="action-button camera" onclick="openCamera()">
                    📷 Take Photo & Post
                </button>
                <button class="action-button secondary" onclick="openPostComposer()">
                    ✍️ Create New Post
                </button>
            </div>
            
            <div class="feature-grid">
                <button class="feature-card" onclick="showAnalytics()">
                    <span class="feature-icon">📊</span>
                    <div class="feature-title">Analytics</div>
                    <div class="feature-desc">Track engagement</div>
                </button>
                
                <button class="feature-card" onclick="showSchedule()">
                    <span class="feature-icon">📅</span>
                    <div class="feature-title">Schedule</div>
                    <div class="feature-desc">Manage posts</div>
                </button>
                
                <button class="feature-card" onclick="showConnections()">
                    <span class="feature-icon">🔗</span>
                    <div class="feature-title">Accounts</div>
                    <div class="feature-desc">Social media</div>
                </button>
                
                <button class="feature-card" onclick="showSettings()">
                    <span class="feature-icon">⚙️</span>
                    <div class="feature-title">Settings</div>
                    <div class="feature-desc">App preferences</div>
                </button>
            </div>
            
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card">
                    <div class="stat-number" id="totalPosts">0</div>
                    <div class="stat-label">Total Posts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalEngagement">0</div>
                    <div class="stat-label">Engagement</div>
                </div>
            </div>
        </div>
        
        <div class="bottom-nav">
            <a href="#" class="nav-item active" onclick="showHome()">
                <span class="nav-icon">🏠</span>
                Home
            </a>
            <a href="#" class="nav-item" onclick="showPosts()">
                <span class="nav-icon">📝</span>
                Posts
            </a>
            <a href="#" class="nav-item" onclick="showCamera()">
                <span class="nav-icon">📷</span>
                Camera
            </a>
            <a href="#" class="nav-item" onclick="showProfile()">
                <span class="nav-icon">👤</span>
                Profile
            </a>
        </div>
    </div>
    
    <!-- Camera Modal -->
    <div class="modal" id="cameraModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">📷 Take Photo</div>
                <button class="close-btn" onclick="closeCameraModal()">&times;</button>
            </div>
            
            <div class="camera-container">
                <div class="camera-preview" id="cameraPreview">
                    📷 Tap to take photo or select from gallery
                </div>
                <input type="file" class="camera-input" id="cameraInput" accept="image/*" capture="environment">
            </div>
            
            <div class="form-group">
                <label class="form-label">Caption</label>
                <textarea class="form-textarea" id="photoCaption" placeholder="Write a caption for your photo..."></textarea>
            </div>
            
            <div class="form-group">
                <label class="form-label">Post to:</label>
                <div class="platform-selector">
                    <div class="platform-option selected" data-platform="facebook">📘 Facebook</div>
                    <div class="platform-option selected" data-platform="instagram">📸 Instagram</div>
                    <div class="platform-option" data-platform="tiktok">🎵 TikTok</div>
                    <div class="platform-option" data-platform="twitter">🐦 Twitter</div>
                </div>
            </div>
            
            <button class="action-button" onclick="publishPhoto()">
                🚀 Publish Now
            </button>
        </div>
    </div>
    
    <!-- Post Composer Modal -->
    <div class="modal" id="postModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">✍️ Create Post</div>
                <button class="close-btn" onclick="closePostModal()">&times;</button>
            </div>
            
            <div class="form-group">
                <label class="form-label">Content</label>
                <textarea class="form-textarea" id="postContent" placeholder="What's happening at your restaurant?"></textarea>
            </div>
            
            <div class="form-group">
                <button class="action-button secondary" onclick="generateAIContent()">
                    🤖 Generate AI Content
                </button>
            </div>
            
            <div class="form-group">
                <label class="form-label">Post to:</label>
                <div class="platform-selector">
                    <div class="platform-option selected" data-platform="facebook">📘 Facebook</div>
                    <div class="platform-option selected" data-platform="instagram">📸 Instagram</div>
                    <div class="platform-option" data-platform="tiktok">🎵 TikTok</div>
                    <div class="platform-option" data-platform="twitter">🐦 Twitter</div>
                </div>
            </div>
            
            <button class="action-button" onclick="publishPost()">
                🚀 Publish Now
            </button>
            <button class="action-button secondary" onclick="schedulePost()">
                📅 Schedule for Later
            </button>
        </div>
    </div>
    
    <!-- Loading Indicator -->
    <div class="loading" id="loadingIndicator">
        <div class="spinner"></div>
        <div>Processing...</div>
    </div>
    
    <!-- Notification -->
    <div class="notification" id="notification"></div>
    
    <script>
        // Service Worker Registration
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => console.log('SW registered'))
                .catch(error => console.log('SW registration failed'));
        }
        
        // App State
        let currentUser = null;
        let selectedPlatforms = ['facebook', 'instagram'];
        let isOnline = navigator.onLine;
        
        // Initialize App
        document.addEventListener('DOMContentLoaded', function() {
            loadUserInfo();
            loadStats();
            setupEventListeners();
            checkOnlineStatus();
        });
        
        // Event Listeners
        function setupEventListeners() {
            // Platform selector
            document.querySelectorAll('.platform-option').forEach(option => {
                option.addEventListener('click', function() {
                    this.classList.toggle('selected');
                    updateSelectedPlatforms();
                });
            });
            
            // Camera input
            document.getElementById('cameraInput').addEventListener('change', handlePhotoCapture);
            
            // Online/Offline detection
            window.addEventListener('online', () => {
                isOnline = true;
                hideOfflineIndicator();
                syncOfflineData();
            });
            
            window.addEventListener('offline', () => {
                isOnline = false;
                showOfflineIndicator();
            });
        }
        
        // User Info
        async function loadUserInfo() {
            try {
                const response = await fetch('/api/mobile/user');
                if (response.ok) {
                    const user = await response.json();
                    currentUser = user;
                    document.getElementById('userInfo').textContent = `${user.name} • ${user.restaurant_name}`;
                } else {
                    document.getElementById('userInfo').textContent = 'Guest User';
                }
            } catch (error) {
                document.getElementById('userInfo').textContent = 'Offline Mode';
            }
        }
        
        // Load Stats
        async function loadStats() {
            try {
                const response = await fetch('/api/mobile/stats');
                if (response.ok) {
                    const stats = await response.json();
                    document.getElementById('totalPosts').textContent = stats.total_posts || 0;
                    document.getElementById('totalEngagement').textContent = stats.total_engagement || 0;
                }
            } catch (error) {
                console.log('Failed to load stats');
            }
        }
        
        // Camera Functions
        function openCamera() {
            document.getElementById('cameraModal').style.display = 'block';
        }
        
        function closeCameraModal() {
            document.getElementById('cameraModal').style.display = 'none';
        }
        
        function handlePhotoCapture(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('cameraPreview');
                    preview.innerHTML = `<img src="${e.target.result}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">`;
                    
                    // Auto-generate AI caption when photo is selected
                    generateAICaptionForPhoto(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        }
        
        async function generateAICaptionForPhoto(imageDataUrl) {
            const captionField = document.getElementById('photoCaption');
            captionField.placeholder = 'Analyzing photo with AI...';
            captionField.value = '';
            
            try {
                // Extract base64 data from data URL
                const base64Data = imageDataUrl.split(',')[1];
                
                const response = await fetch('/api/mobile/generate-photo-caption', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        type: 'food_photo',
                        image_base64: base64Data
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    captionField.value = data.caption;
                    captionField.placeholder = 'AI caption generated! Edit if needed...';
                    showNotification('🤖 AI analyzed your photo and generated a caption!');
                } else {
                    throw new Error('Failed to generate caption');
                }
            } catch (error) {
                console.log('Failed to generate AI caption:', error);
                // Fallback to generating caption without image analysis
                generateFallbackCaption();
            }
        }
        
        async function generateFallbackCaption() {
            const captionField = document.getElementById('photoCaption');
            captionField.placeholder = 'Generating caption...';
            
            try {
                const response = await fetch('/api/mobile/generate-photo-caption', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: 'food_photo' })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    captionField.value = data.caption;
                    captionField.placeholder = 'Caption generated! Edit if needed...';
                    showNotification('📝 Caption generated!');
                } else {
                    throw new Error('Failed to generate caption');
                }
            } catch (error) {
                captionField.placeholder = 'Write a caption for your photo...';
                console.log('Failed to generate caption:', error);
            }
        }
        
        async function publishPhoto() {
            const caption = document.getElementById('photoCaption').value;
            const fileInput = document.getElementById('cameraInput');
            
            if (!fileInput.files[0]) {
                showNotification('Please select a photo first', 'error');
                return;
            }
            
            showLoading();
            
            try {
                const formData = new FormData();
                formData.append('photo', fileInput.files[0]);
                formData.append('caption', caption);
                formData.append('platforms', JSON.stringify(selectedPlatforms));
                
                const response = await fetch('/api/mobile/publish-photo', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    showNotification('📷 Photo published successfully!');
                    closeCameraModal();
                    loadStats();
                } else {
                    throw new Error('Failed to publish photo');
                }
            } catch (error) {
                if (!isOnline) {
                    saveOfflineData('photo', { caption, platforms: selectedPlatforms });
                    showNotification('📱 Saved offline. Will publish when connected.');
                } else {
                    showNotification('Failed to publish photo', 'error');
                }
            } finally {
                hideLoading();
            }
        }
        
        // Post Composer
        function openPostComposer() {
            document.getElementById('postModal').style.display = 'block';
        }
        
        function closePostModal() {
            document.getElementById('postModal').style.display = 'none';
        }
        
        async function generateAIContent() {
            showLoading();
            
            try {
                const response = await fetch('/api/mobile/generate-content', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: 'restaurant_post' })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('postContent').value = data.content;
                    showNotification('🤖 AI content generated!');
                } else {
                    throw new Error('Failed to generate content');
                }
            } catch (error) {
                showNotification('Failed to generate AI content', 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function publishPost() {
            const content = document.getElementById('postContent').value;
            
            if (!content.trim()) {
                showNotification('Please enter some content', 'error');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/api/mobile/publish-post', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        content: content,
                        platforms: selectedPlatforms,
                        schedule_time: null
                    })
                });
                
                if (response.ok) {
                    showNotification('🚀 Post published successfully!');
                    closePostModal();
                    loadStats();
                } else {
                    throw new Error('Failed to publish post');
                }
            } catch (error) {
                if (!isOnline) {
                    saveOfflineData('post', { content, platforms: selectedPlatforms });
                    showNotification('📱 Saved offline. Will publish when connected.');
                } else {
                    showNotification('Failed to publish post', 'error');
                }
            } finally {
                hideLoading();
            }
        }
        
        // Platform Selection
        function updateSelectedPlatforms() {
            selectedPlatforms = Array.from(document.querySelectorAll('.platform-option.selected'))
                .map(option => option.dataset.platform);
        }
        
        // Navigation
        function showHome() {
            updateNavigation('home');
        }
        
        function showPosts() {
            updateNavigation('posts');
            // Load posts view
        }
        
        function showCamera() {
            updateNavigation('camera');
            openCamera();
        }
        
        function showProfile() {
            updateNavigation('profile');
            // Load profile view
        }
        
        function updateNavigation(active) {
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            document.querySelector(`[onclick="show${active.charAt(0).toUpperCase() + active.slice(1)}()"]`).classList.add('active');
        }
        
        // Feature Functions
        function showAnalytics() {
            showNotification('📊 Analytics feature coming soon!');
        }
        
        function showSchedule() {
            showNotification('📅 Schedule feature coming soon!');
        }
        
        function showConnections() {
            showNotification('🔗 Social connections feature coming soon!');
        }
        
        function showSettings() {
            showNotification('⚙️ Settings feature coming soon!');
        }
        
        // Utility Functions
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type}`;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        function showLoading() {
            document.getElementById('loadingIndicator').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loadingIndicator').style.display = 'none';
        }
        
        function showOfflineIndicator() {
            document.getElementById('offlineIndicator').classList.add('show');
        }
        
        function hideOfflineIndicator() {
            document.getElementById('offlineIndicator').classList.remove('show');
        }
        
        function checkOnlineStatus() {
            if (!isOnline) {
                showOfflineIndicator();
            }
        }
        
        // Offline Data Management
        function saveOfflineData(type, data) {
            const offlineData = JSON.parse(localStorage.getItem('offlineData') || '[]');
            offlineData.push({
                type: type,
                data: data,
                timestamp: new Date().toISOString()
            });
            localStorage.setItem('offlineData', JSON.stringify(offlineData));
        }
        
        async function syncOfflineData() {
            const offlineData = JSON.parse(localStorage.getItem('offlineData') || '[]');
            
            if (offlineData.length > 0) {
                showNotification('📡 Syncing offline data...');
                
                for (const item of offlineData) {
                    try {
                        if (item.type === 'post') {
                            await fetch('/api/mobile/publish-post', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(item.data)
                            });
                        }
                        // Handle other types as needed
                    } catch (error) {
                        console.log('Failed to sync item:', error);
                    }
                }
                
                localStorage.removeItem('offlineData');
                showNotification('✅ Offline data synced successfully!');
                loadStats();
            }
        }
        
        // Push Notifications (if supported)
        if ('Notification' in window && 'serviceWorker' in navigator) {
            Notification.requestPermission();
        }
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
def mobile_app():
    return render_template_string(MOBILE_APP_TEMPLATE)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Restaurant Social - Mobile App",
        "short_name": "RestaurantSocial",
        "description": "Professional social media management for restaurants",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#6366f1",
        "theme_color": "#6366f1",
        "orientation": "portrait",
        "icons": [
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 192 192'><rect width='192' height='192' fill='%236366f1'/><text y='96' x='96' text-anchor='middle' dy='0.35em' font-size='96' fill='white'>🍽️</text></svg>",
                "sizes": "192x192",
                "type": "image/svg+xml"
            },
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'><rect width='512' height='512' fill='%236366f1'/><text y='256' x='256' text-anchor='middle' dy='0.35em' font-size='256' fill='white'>🍽️</text></svg>",
                "sizes": "512x512",
                "type": "image/svg+xml"
            }
        ]
    })

@app.route('/sw.js')
def service_worker():
    sw_content = '''
const CACHE_NAME = 'restaurant-social-v1';
const urlsToCache = [
    '/',
    '/manifest.json'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});

self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(syncOfflineData());
    }
});

async function syncOfflineData() {
    // Sync offline data when connection is restored
    console.log('Syncing offline data...');
}
'''
    return sw_content, 200, {'Content-Type': 'application/javascript'}

# API Routes
@app.route('/api/mobile/user')
def get_mobile_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.name, u.email, r.name as restaurant_name
        FROM users u
        LEFT JOIN restaurants r ON u.id = r.user_id
        WHERE u.id = ?
    ''', (session['user_id'],))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return jsonify({
            'name': user_data[0],
            'email': user_data[1],
            'restaurant_name': user_data[2] or 'My Restaurant'
        })
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/mobile/stats')
def get_mobile_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    # Get restaurant ID
    cursor.execute('SELECT id FROM restaurants WHERE user_id = ?', (session['user_id'],))
    restaurant = cursor.fetchone()
    
    if not restaurant:
        return jsonify({'total_posts': 0, 'total_engagement': 0})
    
    restaurant_id = restaurant[0]
    
    # Get stats
    cursor.execute('SELECT COUNT(*) FROM posts WHERE restaurant_id = ?', (restaurant_id,))
    total_posts = cursor.fetchone()[0]
    
    # Mock engagement data
    total_engagement = total_posts * 25  # Simulate engagement
    
    conn.close()
    
    return jsonify({
        'total_posts': total_posts,
        'total_engagement': total_engagement
    })

@app.route('/api/mobile/generate-photo-caption', methods=['POST'])
def generate_photo_caption():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get restaurant context for the user
        conn = sqlite3.connect('restaurant_social_mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.name, r.cuisine, r.description, r.location
            FROM restaurants r
            JOIN users u ON r.user_id = u.id
            WHERE u.id = ?
        ''', (session['user_id'],))
        
        restaurant_data = cursor.fetchone()
        conn.close()
        
        restaurant_context = {}
        if restaurant_data:
            restaurant_context = {
                'name': restaurant_data[0],
                'cuisine': restaurant_data[1] or 'International',
                'style': 'Restaurant',
                'location': restaurant_data[3] or 'Local'
            }
        
        # Check if image data is provided
        data = request.get_json() or {}
        image_base64 = data.get('image_base64')
        
        if image_base64:
            # Use AI to analyze the image and generate caption
            caption = ai_caption_generator.generate_caption_from_image(
                image_base64, 
                restaurant_context, 
                caption_style="engaging"
            )
        else:
            # Generate fallback caption with restaurant context
            caption = ai_caption_generator._generate_fallback_caption(restaurant_context)
        
        return jsonify({'caption': caption})
        
    except Exception as e:
        print(f"Error generating AI caption: {e}")
        
        # Fallback to simple captions if AI fails
        food_captions = [
            "🍽️ Fresh from our kitchen to your table! Every bite tells a story of passion and flavor. #FreshFood #RestaurantLife #Foodie #Delicious",
            "👨‍🍳 Our chef's masterpiece is ready to delight your senses. Made with love and the finest ingredients! #ChefSpecial #FineDining #FoodArt #Gourmet",
            "🌟 Today's special is more than just a meal - it's an experience! Come taste the difference quality makes. #TodaysSpecial #QualityFood #RestaurantExperience",
            "✨ Every dish is crafted with attention to detail and a sprinkle of culinary magic! #CraftedWithLove #CulinaryMagic #AttentionToDetail #FoodCraftsmanship"
        ]
        
        import random
        caption = random.choice(food_captions)
        
        return jsonify({'caption': caption})

@app.route('/api/mobile/generate-content', methods=['POST'])
def generate_mobile_content():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get restaurant context for the user
        conn = sqlite3.connect('restaurant_social_mobile.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.name, r.cuisine, r.description, r.location
            FROM restaurants r
            JOIN users u ON r.user_id = u.id
            WHERE u.id = ?
        ''', (session['user_id'],))
        
        restaurant_data = cursor.fetchone()
        conn.close()
        
        restaurant_context = {}
        if restaurant_data:
            restaurant_context = {
                'name': restaurant_data[0],
                'cuisine': restaurant_data[1] or 'International',
                'style': 'Restaurant',
                'location': restaurant_data[3] or 'Local'
            }
        
        # Generate AI content for restaurant posts
        try:
            content = ai_caption_generator.generate_ai_content(restaurant_context)
            return jsonify({'content': content})
            
        except Exception as ai_error:
            print(f"AI content generation failed: {ai_error}")
            # Fallback to predefined content
            raise ai_error
            
    except Exception as e:
        print(f"Error generating AI content: {e}")
        
        # Fallback AI content suggestions for restaurants
        ai_suggestions = [
            "🍽️ Fresh ingredients, amazing flavors! Come taste the difference at our restaurant. #FreshFood #LocalDining #RestaurantLife #Foodie #ChefSpecial",
            "👨‍🍳 Our chef's special creations are waiting for you. Book your table today! #ChefSpecial #FineDining #Foodie #CulinaryArt #RestaurantExperience",
            "🌟 Thank you to all our amazing customers! Your support means everything to us. #Grateful #Community #Restaurant #CustomerLove #LocalSupport",
            "🥘 New menu items just dropped! Our latest creations are ready to delight your taste buds. #NewMenu #Innovation #Delicious #FoodieAlert #TasteBuds",
            "📸 Behind the scenes in our kitchen - where the magic happens! #BehindTheScenes #Kitchen #Passion #CulinaryMagic #ChefLife",
            "🎉 Weekend special: Join us for an unforgettable dining experience! #WeekendSpecial #Dining #Experience #RestaurantLife #SpecialOffer"
        ]
        
        import random
        content = random.choice(ai_suggestions)
        
        return jsonify({'content': content})

@app.route('/api/mobile/publish-post', methods=['POST'])
def publish_mobile_post():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    content = data.get('content', '')
    platforms = data.get('platforms', [])
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    # Get restaurant ID
    cursor.execute('SELECT id FROM restaurants WHERE user_id = ?', (session['user_id'],))
    restaurant = cursor.fetchone()
    
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    restaurant_id = restaurant[0]
    
    # Save post
    cursor.execute('''
        INSERT INTO posts (restaurant_id, content, platforms, status)
        VALUES (?, ?, ?, ?)
    ''', (restaurant_id, content, json.dumps(platforms), 'published'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Post published successfully'})

@app.route('/api/mobile/publish-photo', methods=['POST'])
def publish_mobile_photo():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    caption = request.form.get('caption', '')
    platforms = json.loads(request.form.get('platforms', '[]'))
    photo = request.files.get('photo')
    
    if not photo:
        return jsonify({'error': 'Photo is required'}), 400
    
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    # Get restaurant ID
    cursor.execute('SELECT id FROM restaurants WHERE user_id = ?', (session['user_id'],))
    restaurant = cursor.fetchone()
    
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    restaurant_id = restaurant[0]
    
    # In a real app, you would save the photo to cloud storage
    # For demo, we'll just save the post with a placeholder
    photo_url = f"photo_{datetime.datetime.now().timestamp()}.jpg"
    
    # Save post with photo
    cursor.execute('''
        INSERT INTO posts (restaurant_id, content, media_urls, platforms, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (restaurant_id, caption, json.dumps([photo_url]), json.dumps(platforms), 'published'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Photo published successfully'})

# Authentication routes (simplified for mobile)
@app.route('/api/mobile/login', methods=['POST'])
def mobile_login():
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password_hash FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    if user and user[1] == hash_password(password):
        session['user_id'] = user[0]
        conn.close()
        return jsonify({'success': True})
    
    conn.close()
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/mobile/register', methods=['POST'])
def mobile_register():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    password = data.get('password', '')
    restaurant_name = data.get('restaurant_name', '')
    
    if not all([name, email, password, restaurant_name]):
        return jsonify({'error': 'All fields required'}), 400
    
    conn = sqlite3.connect('restaurant_social_mobile.db')
    cursor = conn.cursor()
    
    try:
        # Create user
        cursor.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        ''', (name, email, hash_password(password)))
        
        user_id = cursor.lastrowid
        
        # Create restaurant
        cursor.execute('''
            INSERT INTO restaurants (user_id, name, description, cuisine, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, restaurant_name, f"A wonderful restaurant owned by {name}", "International", "Your City"))
        
        conn.commit()
        session['user_id'] = user_id
        
        conn.close()
        return jsonify({'success': True})
        
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already registered'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

