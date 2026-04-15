<template>
  <div class="auth-wrapper" :class="theme">
    <div class="bg-grid"></div>
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>
    <div class="bg-orb orb-3"></div>

    <!-- Theme toggle -->
    <button class="theme-toggle" @click="$emit('toggleTheme')" :title="theme === 'dark' ? 'Светлая тема' : 'Тёмная тема'">
      <svg v-if="theme === 'dark'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>
      <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
    </button>

    <div class="auth-container">
      <div class="brand" :class="{ 'brand-visible': mounted }">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="14" stroke="url(#g1)" stroke-width="2"/>
            <path d="M10 16 L14 20 L22 12" stroke="url(#g1)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="g1" x1="0" y1="0" x2="32" y2="32">
                <stop offset="0%" stop-color="#4f8ef7"/>
                <stop offset="100%" stop-color="#a855f7"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span class="brand-name">HabitsLine</span>
      </div>

      <div class="tab-switcher" :class="{ 'tabs-visible': mounted }">
        <button class="tab-btn" :class="{ active: mode === 'login' }" @click="switchMode('login')">Войти</button>
        <button class="tab-btn" :class="{ active: mode === 'register' }" @click="switchMode('register')">Регистрация</button>
        <div class="tab-indicator" :class="{ 'tab-right': mode === 'register' }"></div>
      </div>

      <div class="card" :class="{ 'card-visible': mounted }">
        <transition name="slide-fade" mode="out-in">
          <div v-if="mode === 'login'" key="login" class="form-section">
            <h2 class="form-title">С возвращением</h2>
            <p class="form-subtitle">Войдите, чтобы продолжить</p>

            <div class="field" :class="{ focused: focused === 'lemail', filled: loginEmail }">
              <label>Email</label>
              <input type="email" v-model="loginEmail" @focus="focused = 'lemail'" @blur="focused = null" placeholder="you@example.com"/>
              <div class="field-line"></div>
              <p v-if="loginEmailHint" class="input-hint">{{ loginEmailHint }}</p>
            </div>

            <div class="field" :class="{ focused: focused === 'lpass', filled: loginPassword }">
              <label>Пароль</label>
              <input :type="showLoginPass ? 'text' : 'password'" v-model="loginPassword" @focus="focused = 'lpass'" @blur="focused = null" placeholder="••••••••"/>
              <button type="button" class="eye-btn" @click="showLoginPass = !showLoginPass">
                <svg v-if="showLoginPass" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
              <div class="field-line"></div>
            </div>

            <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

            <button class="submit-btn" @click="login" :disabled="loading">
              <span v-if="!loading">Войти</span>
              <span v-else class="spinner"></span>
            </button>

            <p class="switch-hint">Нет аккаунта? <button class="link-btn" @click="switchMode('register')">Зарегистрироваться</button></p>
          </div>
        </transition>

        <transition name="slide-fade" mode="out-in">
          <div v-if="mode === 'register'" key="register" class="form-section">
            <h2 class="form-title">Создать аккаунт</h2>
            <p class="form-subtitle">Начните отслеживать привычки</p>

            <div class="field" :class="{ focused: focused === 'rname', filled: registerName }">
              <label>Имя</label>
              <input type="text" v-model="registerName" @focus="focused = 'rname'" @blur="focused = null" placeholder="Как вас зовут?"/>
              <div class="field-line"></div>
            </div>

            <div class="field" :class="{ focused: focused === 'rage', filled: registerAge }">
              <label>Возраст</label>
              <input type="number" v-model="registerAge" @focus="focused = 'rage'" @blur="focused = null" placeholder="25" min="1" max="120"/>
              <div class="field-line"></div>
            </div>

            <div class="field" :class="{ focused: focused === 'remail', filled: registerEmail }">
              <label>Email</label>
              <input type="email" v-model="registerEmail" @focus="focused = 'remail'" @blur="focused = null" placeholder="you@example.com"/>
              <div class="field-line"></div>
              <p v-if="registerEmailHint" class="input-hint">{{ registerEmailHint }}</p>
            </div>

            <div class="field" :class="{ focused: focused === 'rpass', filled: registerPassword }">
              <label>Пароль</label>
              <input :type="showRegPass ? 'text' : 'password'" v-model="registerPassword" @focus="focused = 'rpass'" @blur="focused = null" placeholder="Минимум 8 символов"/>
              <button type="button" class="eye-btn" @click="showRegPass = !showRegPass">
                <svg v-if="showRegPass" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
              <div class="field-line"></div>
              <p v-if="registerPasswordHint" class="input-hint">{{ registerPasswordHint }}</p>
            </div>

            <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
            <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>

            <button class="submit-btn" @click="register" :disabled="loading">
              <span v-if="!loading">Создать аккаунт</span>
              <span v-else class="spinner"></span>
            </button>

            <p class="switch-hint">Уже есть аккаунт? <button class="link-btn" @click="switchMode('login')">Войти</button></p>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API = '/api';
const TOKEN_KEY = 'access_token';

export default {
  name: 'AuthComponent',
  props: { theme: { type: String, default: 'dark' } },
  emits: ['handleAuth', 'toggleTheme'],
  data() {
    return {
      mode: 'login',
      mounted: false,
      focused: null,
      loading: false,
      errorMsg: '',
      successMsg: '',
      showLoginPass: false,
      showRegPass: false,
      loginEmail: '',
      loginPassword: '',
      registerName: '',
      registerAge: '',
      registerEmail: '',
      registerPassword: '',
    };
  },
  computed: {
    loginEmailHint() {
      const value = this.loginEmail.trim();
      if (!value) return 'Введите email в формате name@example.com';
      if (!this.isValidEmail(value)) return 'Неверный формат email';
      return 'Email выглядит корректно';
    },
    registerEmailHint() {
      const value = this.registerEmail.trim();
      if (!value) return 'Используйте действующий email';
      if (!this.isValidEmail(value)) return 'Проверьте формат, например name@example.com';
      return 'Email выглядит корректно';
    },
    registerPasswordHint() {
      if (!this.registerPassword) return 'Минимум 8 символов';
      if (this.registerPassword.length < 8) return `Ещё ${8 - this.registerPassword.length} символ(ов)`;
      return 'Пароль подходит по длине';
    },
  },
  mounted() {
    setTimeout(() => { this.mounted = true; }, 50);
  },
  methods: {
    isValidEmail(email) {
      const value = String(email || '').trim().toLowerCase();
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    },
    switchMode(mode) {
      this.mode = mode;
      this.errorMsg = '';
      this.successMsg = '';
    },
    async login() {
      this.errorMsg = '';
      const email = this.loginEmail.trim().toLowerCase();
      if (!email || !this.loginPassword) { this.errorMsg = 'Заполните все поля'; return; }
      if (!this.isValidEmail(email)) { this.errorMsg = 'Введите корректный email'; return; }
      this.loading = true;
      try {
        const { data } = await axios.post(`${API}/auth/login`, {
          email,
          password: this.loginPassword,
        }, { withCredentials: true });
        const token = data?.access_token;
        if (!token) throw new Error('No access token returned');
        localStorage.setItem(TOKEN_KEY, token);
        const { data: user } = await axios.get(`${API}/users/me`, {
          withCredentials: true,
          headers: { Authorization: `Bearer ${token}` },
        });
        this.$emit('handleAuth', user);
      } catch (e) {
        this.errorMsg = e.response?.data?.detail || 'Неверный email или пароль';
      } finally {
        this.loading = false;
      }
    },
    async register() {
      this.errorMsg = '';
      this.successMsg = '';
      const email = this.registerEmail.trim().toLowerCase();
      if (!this.registerName || !this.registerAge || !email || !this.registerPassword) {
        this.errorMsg = 'Заполните все поля'; return;
      }
      if (!this.isValidEmail(email)) { this.errorMsg = 'Введите корректный email'; return; }
      this.loading = true;
      try {
        await axios.post(`${API}/auth/register`, {
          name: this.registerName,
          age: Number(this.registerAge),
          email,
          password: this.registerPassword,
        });
        this.successMsg = 'Аккаунт создан! Войдите.';
        setTimeout(() => this.switchMode('login'), 1500);
      } catch (e) {
        this.errorMsg = e.response?.data?.detail || 'Ошибка регистрации. Попробуйте снова.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── CSS Variables ─────────────────────────────── */
.auth-wrapper.dark {
  --bg: #050508;
  --bg-card: rgba(10,12,25,0.85);
  --border: rgba(79,142,247,0.18);
  --border-tab: rgba(79,142,247,0.15);
  --text: #ffffff;
  --text-sub: rgba(255,255,255,0.35);
  --text-label: rgba(255,255,255,0.35);
  --input-bg: rgba(255,255,255,0.04);
  --input-border: rgba(255,255,255,0.08);
  --tab-bg: rgba(255,255,255,0.04);
  --tab-inactive: rgba(255,255,255,0.4);
  --toggle-bg: rgba(255,255,255,0.08);
  --toggle-color: rgba(255,255,255,0.6);
  --orb-opacity: 0.18;
  --grid-color: rgba(79,142,247,0.04);
  --shadow: 0 24px 60px rgba(0,0,0,0.5);
}
.auth-wrapper.light {
  --bg: #f0f4ff;
  --bg-card: rgba(255,255,255,0.95);
  --border: rgba(79,142,247,0.25);
  --border-tab: rgba(79,142,247,0.2);
  --text: #0f1729;
  --text-sub: rgba(15,23,41,0.45);
  --text-label: rgba(15,23,41,0.45);
  --input-bg: rgba(79,142,247,0.04);
  --input-border: rgba(79,142,247,0.15);
  --tab-bg: rgba(79,142,247,0.06);
  --tab-inactive: rgba(15,23,41,0.4);
  --toggle-bg: rgba(79,142,247,0.1);
  --toggle-color: #4f8ef7;
  --orb-opacity: 0.1;
  --grid-color: rgba(79,142,247,0.06);
  --shadow: 0 24px 60px rgba(79,142,247,0.12);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.auth-wrapper {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Sans', sans-serif;
  overflow: hidden;
  position: relative;
  transition: background 0.4s ease;
}

.bg-grid {
  position: fixed; inset: 0;
  background-image:
    linear-gradient(var(--grid-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
  background-size: 48px 48px;
  animation: gridShift 20s linear infinite;
  transition: opacity 0.4s;
}
@keyframes gridShift { 0% { transform: translateY(0); } 100% { transform: translateY(48px); } }

.bg-orb {
  position: fixed; border-radius: 50%;
  filter: blur(80px);
  opacity: var(--orb-opacity);
  animation: orbFloat 12s ease-in-out infinite;
  transition: opacity 0.4s;
}
.orb-1 { width: 500px; height: 500px; background: radial-gradient(circle, #4f8ef7, transparent 70%); top: -150px; left: -100px; }
.orb-2 { width: 400px; height: 400px; background: radial-gradient(circle, #a855f7, transparent 70%); bottom: -100px; right: -80px; animation-delay: -4s; }
.orb-3 { width: 300px; height: 300px; background: radial-gradient(circle, #3b82f6, transparent 70%); top: 50%; left: 60%; animation-delay: -8s; }
@keyframes orbFloat {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(30px,-20px) scale(1.05); }
  66% { transform: translate(-20px,30px) scale(0.95); }
}

/* Theme toggle */
.theme-toggle {
  position: fixed; top: 20px; right: 20px; z-index: 100;
  width: 40px; height: 40px;
  border-radius: 10px;
  background: var(--toggle-bg);
  border: 1px solid var(--border);
  color: var(--toggle-color);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}
.theme-toggle:hover { transform: scale(1.1); }

.auth-container {
  position: relative; z-index: 10;
  width: 100%; max-width: 420px;
  padding: 0 20px;
  display: flex; flex-direction: column; align-items: center; gap: 24px;
}

.brand {
  display: flex; align-items: center; gap: 12px;
  opacity: 0; transform: translateY(-20px);
  transition: all 0.6s cubic-bezier(0.34,1.56,0.64,1);
}
.brand.brand-visible { opacity: 1; transform: translateY(0); }
.brand-icon {
  display: flex; align-items: center; justify-content: center;
  width: 44px; height: 44px; border-radius: 12px;
  background: rgba(79,142,247,0.1);
  border: 1px solid rgba(79,142,247,0.2);
}
.brand-name {
  font-family: 'Syne', sans-serif;
  font-size: 24px; font-weight: 800;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  letter-spacing: -0.5px;
}

.tab-switcher {
  position: relative; display: flex;
  background: var(--tab-bg);
  border: 1px solid var(--border-tab);
  border-radius: 12px; padding: 4px; width: 100%;
  opacity: 0; transform: translateY(-10px);
  transition: all 0.6s cubic-bezier(0.34,1.56,0.64,1) 0.15s;
}
.tab-switcher.tabs-visible { opacity: 1; transform: translateY(0); }
.tab-btn {
  flex: 1; padding: 10px; border: none; background: transparent;
  color: var(--tab-inactive);
  font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 500;
  cursor: pointer; border-radius: 9px; position: relative; z-index: 2;
  transition: color 0.3s;
}
.tab-btn.active { color: var(--text); }
.tab-indicator {
  position: absolute; top: 4px; left: 4px;
  width: calc(50% - 4px); height: calc(100% - 8px);
  background: linear-gradient(135deg, rgba(79,142,247,0.3), rgba(168,85,247,0.3));
  border: 1px solid rgba(79,142,247,0.4);
  border-radius: 9px;
  transition: transform 0.35s cubic-bezier(0.34,1.4,0.64,1);
  backdrop-filter: blur(4px);
}
.tab-indicator.tab-right { transform: translateX(100%); }

.card {
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 24px; padding: 36px 32px;
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow);
  opacity: 0; transform: translateY(20px);
  transition: all 0.7s cubic-bezier(0.34,1.2,0.64,1) 0.25s, background 0.4s, border-color 0.4s;
  min-height: 360px;
}
.card.card-visible { opacity: 1; transform: translateY(0); }

.form-section { width: 100%; }
.form-title {
  font-family: 'Syne', sans-serif;
  font-size: 26px; font-weight: 700; color: var(--text);
  margin-bottom: 6px; letter-spacing: -0.5px;
}
.form-subtitle { font-size: 14px; color: var(--text-sub); margin-bottom: 28px; }

.field { position: relative; margin-bottom: 22px; }
.field label {
  display: block; font-size: 11px; font-weight: 600;
  color: var(--text-label); margin-bottom: 8px;
  letter-spacing: 0.8px; text-transform: uppercase;
  transition: color 0.3s;
}
.field.focused label, .field.filled label { color: #4f8ef7; }
.field input {
  width: 100%;
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: 10px; padding: 13px 40px 13px 16px;
  color: var(--text);
  font-family: 'DM Sans', sans-serif; font-size: 15px; outline: none;
  transition: all 0.3s;
}
.field input::placeholder { color: var(--text-sub); }
.field.focused input {
  border-color: rgba(79,142,247,0.5);
  background: rgba(79,142,247,0.06);
  box-shadow: 0 0 0 3px rgba(79,142,247,0.1);
}
.field-line {
  position: absolute; bottom: 0; left: 16px; right: 16px;
  height: 2px;
  background: linear-gradient(90deg, #4f8ef7, #a855f7);
  transform: scaleX(0); transform-origin: left;
  transition: transform 0.4s cubic-bezier(0.34,1.2,0.64,1);
  border-radius: 2px;
}
.field.focused .field-line { transform: scaleX(1); }
.input-hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-sub);
  line-height: 1.35;
}

.eye-btn {
  position: absolute; right: 12px; top: 50%;
  transform: translateY(8%);
  background: none; border: none; cursor: pointer;
  color: var(--text-sub); opacity: 0.6;
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.2s;
}
.eye-btn:hover { opacity: 1; }

.submit-btn {
  width: 100%; padding: 14px; border: none; border-radius: 12px;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  color: #fff; font-family: 'DM Sans', sans-serif;
  font-size: 15px; font-weight: 600; cursor: pointer; margin-top: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(79,142,247,0.3);
}
.submit-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(79,142,247,0.4); }
.submit-btn:active:not(:disabled) { transform: translateY(0); }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  display: inline-block; width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff;
  border-radius: 50%; animation: spin 0.7s linear infinite; vertical-align: middle;
}
@keyframes spin { to { transform: rotate(360deg); } }

.error-msg {
  color: #f87171; font-size: 13px; margin-bottom: 12px;
  padding: 10px 12px;
  background: rgba(248,113,113,0.08);
  border: 1px solid rgba(248,113,113,0.2);
  border-radius: 8px; animation: shake 0.4s ease;
}
@keyframes shake {
  0%,100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  75% { transform: translateX(6px); }
}
.success-msg {
  color: #4ade80; font-size: 13px; margin-bottom: 12px;
  padding: 10px 12px;
  background: rgba(74,222,128,0.08);
  border: 1px solid rgba(74,222,128,0.2);
  border-radius: 8px;
}

.switch-hint { text-align: center; margin-top: 20px; font-size: 13px; color: var(--text-sub); }
.link-btn {
  background: none; border: none; color: #4f8ef7;
  cursor: pointer; font-size: 13px;
  font-family: 'DM Sans', sans-serif; font-weight: 500;
  transition: color 0.2s; padding: 0;
}
.link-btn:hover { color: #a855f7; }

.slide-fade-enter-active { transition: all 0.35s cubic-bezier(0.34,1.2,0.64,1); }
.slide-fade-leave-active { transition: all 0.2s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateX(24px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-24px); }

/* ── Mobile ─────────────────────────────────────── */
@media (max-width: 480px) {
  .auth-container { padding: 0 16px; gap: 20px; }
  .card { padding: 28px 20px; min-height: auto; }
  .form-title { font-size: 22px; }
  .brand-name { font-size: 20px; }
  .theme-toggle { top: 16px; right: 16px; }
}
</style>
