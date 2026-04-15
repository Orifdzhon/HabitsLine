<template>
  <div id="app" :class="theme">
    <auth-component
      v-if="!isAuth"
      :theme="theme"
      @handleAuth="handleAuth"
      @toggleTheme="toggleTheme"
    />
    <dashboard-component
      v-else
      :user="user"
      :theme="theme"
      @logout="logout"
      @toggleTheme="toggleTheme"
    />
  </div>
</template>

<script>
import axios from 'axios'
import AuthComponent from './components/AuthComponent.vue'
import DashboardComponent from './components/DashboardComponent.vue'
const API = '/api';
const TOKEN_KEY = 'access_token';

export default {
  name: 'App',
  components: { AuthComponent, DashboardComponent },
  data() {
    return {
      isAuth: false,
      user: null,
      theme: 'dark',
    }
  },
  async mounted() {
    await this.restoreSession();
  },
  methods: {
    async restoreSession() {
      const token = localStorage.getItem(TOKEN_KEY);
      if (!token) return;

      try {
        const { data: user } = await axios.get(`${API}/users/me`, {
          withCredentials: true,
          headers: { Authorization: `Bearer ${token}` },
        });
        this.user = user;
        this.isAuth = true;
      } catch (e) {
        localStorage.removeItem(TOKEN_KEY);
        this.user = null;
        this.isAuth = false;
      }
    },
    handleAuth(user) {
      this.user = user;
      this.isAuth = true;
    },
    logout() {
      localStorage.removeItem(TOKEN_KEY);
      this.isAuth = false;
      this.user = null;
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark';
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body { min-height: 100vh; }

#app {
  font-family: 'DM Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  transition: background 0.4s ease;
}
#app.dark { background: #050508; }
#app.light { background: #f0f4ff; }
</style>
