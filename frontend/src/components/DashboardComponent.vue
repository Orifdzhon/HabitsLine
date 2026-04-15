<template>
  <div class="dashboard" :class="theme">
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>

    <!-- ── Sidebar ── -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <div class="brand">
          <div class="brand-icon">
            <svg width="22" height="22" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="14" stroke="url(#gs)" stroke-width="2"/>
              <path d="M10 16 L14 20 L22 12" stroke="url(#gs)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              <defs>
                <linearGradient id="gs" x1="0" y1="0" x2="32" y2="32">
                  <stop offset="0%" stop-color="#4f8ef7"/>
                  <stop offset="100%" stop-color="#a855f7"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <span class="brand-name">HabitsLine</span>
        </div>
        <button class="sidebar-close" @click="sidebarOpen = false">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <nav class="sidebar-nav">
        <button class="nav-item" :class="{ active: page === 'habits' }" @click="page = 'habits'; sidebarOpen = false">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
          Мои привычки
        </button>
        <button class="nav-item" :class="{ active: page === 'profile' }" @click="page = 'profile'; sidebarOpen = false">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Профиль
        </button>
      </nav>

      <div class="sidebar-footer">
        <button class="theme-btn" @click="$emit('toggleTheme')">
          <svg v-if="theme === 'dark'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          {{ theme === 'dark' ? 'Светлая тема' : 'Тёмная тема' }}
        </button>
        <button class="logout-btn" @click="requestLogout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Выйти
        </button>
      </div>
    </aside>

    <!-- Overlay for mobile -->
    <div class="overlay" v-if="sidebarOpen" @click="sidebarOpen = false"></div>

    <!-- ── Main ── -->
    <main class="main">
      <!-- Topbar -->
      <header class="topbar">
        <button class="burger" @click="sidebarOpen = true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <div class="topbar-title">{{ page === 'habits' ? 'Мои привычки' : 'Профиль' }}</div>
        <div class="topbar-avatar" @click="page = 'profile'">{{ user.name[0].toUpperCase() }}</div>
      </header>

      <!-- ── HABITS PAGE ── -->
      <transition name="page-fade" mode="out-in">
        <div v-if="page === 'habits'" key="habits" class="page page-habits">
          <!-- Add habit form -->
          <div class="add-card">
            <h3 class="section-title">Новая привычка</h3>
            <div class="add-form">
              <div class="add-inputs">
                <input class="input" v-model="newHabit.name" placeholder="Название привычки" @keyup.enter="addHabit"/>
                <select class="input select" v-model="newHabit.frequency">
                  <option value="daily">Ежедневно</option>
                  <option value="weekly">Еженедельно</option>
                  <option value="workdays">По будням</option>
                  <option value="custom">Другое</option>
                </select>
              </div>
              <button class="add-btn" @click="addHabit" :disabled="addingHabit">
                <span v-if="!addingHabit">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                  Добавить
                </span>
                <span v-else class="spinner"></span>
              </button>
            </div>
          </div>

          <!-- Habits list -->
          <div class="habits-section">
            <h3 class="section-title">
              Привычки
              <span class="count-badge">{{ habits.length }}</span>
            </h3>

            <div v-if="loadingHabits" class="loading-state">
              <span class="spinner big"></span>
            </div>

            <div v-else-if="habits.length === 0" class="empty-state">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              <p>Нет привычек. Добавьте первую!</p>
            </div>

            <div v-else class="habits-list">
              <div class="month-title">{{ currentMonthLabel }}</div>
              <div class="habits-layout">
                <div class="habits-tables">
                  <div v-for="section in groupedHabits" :key="section.key" class="frequency-section">
                    <h4 class="frequency-title">{{ section.label }}</h4>
                    <div class="month-table-wrap">
                      <table class="month-table">
                        <thead>
                          <tr>
                            <th class="habit-col">Привычка</th>
                            <th
                              v-for="day in monthDays"
                              :key="`${section.key}-${day.key}`"
                              class="day-col"
                              :class="{ today: day.isToday }"
                            >
                              {{ day.day }}
                            </th>
                            <th class="action-col">Удалить</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="habit in section.items" :key="habit.id">
                            <td class="habit-cell">
                              <div class="habit-cell-content">
                                <div class="habit-main">
                                  <span class="habit-name">{{ habit.name }}</span>
                                </div>
                            <button class="edit-btn" @click.stop="openHabitEdit(habit)" title="Редактировать привычку">
                              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 20h9"/>
                                <path d="M16.5 3.5a2.1 2.1 0 113 3L7 19l-4 1 1-4 12.5-12.5z"/>
                              </svg>
                            </button>
                              </div>
                            </td>
                            <td
                              v-for="day in monthDays"
                              :key="`${habit.id}-${day.key}`"
                              class="status-cell"
                              :class="{
                                done: isDone(habit.id, day.date),
                                today: day.isToday,
                                'has-comment': hasDayComment(habit.id, day.date),
                              }"
                              @click="toggleDay(habit, day)"
                            >
                              <span class="status-mark">{{ isDone(habit.id, day.date) ? '✓' : '✕' }}</span>
                              <button
                                type="button"
                                class="comment-chip"
                                :class="{ active: hasDayComment(habit.id, day.date) }"
                                title="Добавить комментарий"
                                aria-label="Добавить комментарий"
                                @click.stop="openCommentModal(habit, day)"
                              >
                                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                                  <polyline points="14 2 14 8 20 8"/>
                                  <line x1="8" y1="13" x2="16" y2="13"/>
                                  <line x1="8" y1="17" x2="12" y2="17"/>
                                </svg>
                              </button>
                            </td>
                            <td class="action-cell">
                              <button class="delete-btn solid" @click.stop="requestDeleteHabit(habit)" title="Удалить привычку">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                <aside class="progress-cards" aria-label="Карточки прогресса">
                  <section class="progress-card" aria-label="Прогресс за сегодня">
                    <h4 class="progress-title">Прогресс за сегодня</h4>
                    <div class="progress-ring-wrap">
                      <svg class="progress-ring" viewBox="0 0 120 120" role="img" aria-label="Круг прогресса за сегодня">
                        <circle class="progress-bg" cx="60" cy="60" :r="progressRingRadius"></circle>
                        <circle
                          class="progress-value"
                          cx="60"
                          cy="60"
                          :r="progressRingRadius"
                          :stroke="todayProgressColor"
                          :stroke-dasharray="progressRingCircumference"
                          :stroke-dashoffset="progressRingOffset"
                        ></circle>
                      </svg>
                      <div class="progress-center">
                        <span class="progress-percent" :style="{ color: todayProgressColor }">{{ todayProgressPercent }}%</span>
                      </div>
                    </div>
                    <p class="progress-meta">{{ todayDoneCount }} / {{ todayTotalCount }} выполнено</p>
                  </section>

                  <section class="progress-card" aria-label="Прогресс за месяц">
                    <h4 class="progress-title">Прогресс за месяц</h4>
                    <div class="progress-ring-wrap">
                      <svg class="progress-ring" viewBox="0 0 120 120" role="img" aria-label="Круг прогресса за месяц">
                        <circle class="progress-bg" cx="60" cy="60" :r="progressRingRadius"></circle>
                        <circle
                          class="progress-value"
                          cx="60"
                          cy="60"
                          :r="progressRingRadius"
                          :stroke="monthProgressColor"
                          :stroke-dasharray="progressRingCircumference"
                          :stroke-dashoffset="monthProgressRingOffset"
                        ></circle>
                      </svg>
                      <div class="progress-center">
                        <span class="progress-percent" :style="{ color: monthProgressColor }">{{ monthProgressPercent }}%</span>
                      </div>
                    </div>
                    <p class="progress-meta">{{ monthDoneCount }} / {{ monthTotalCount }} выполнено</p>
                  </section>
                </aside>
              </div>

              <div v-if="pendingDeleteHabit" class="habit-delete-modal-backdrop">
                <div class="habit-delete-modal">
                  <h4>Удалить привычку?</h4>
                  <p>Привычка <strong>{{ pendingDeleteHabit.name }}</strong> и все её отметки будут удалены.</p>
                  <div class="habit-delete-actions">
                    <button class="cancel-btn" @click="cancelHabitDelete" :disabled="deletingHabit">Отмена</button>
                    <button class="danger-btn" @click="confirmHabitDelete" :disabled="deletingHabit">
                      <span v-if="!deletingHabit">Подтвердить</span>
                      <span v-else class="spinner"></span>
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="habitEditModal" class="habit-delete-modal-backdrop" @click.self="onHabitEditBackdrop">
                <div class="habit-delete-modal">
                  <h4>Редактировать привычку</h4>
                  <div class="edit-form">
                    <div class="field">
                      <label>Название</label>
                      <input class="input" v-model="habitEditForm.name" placeholder="Название привычки"/>
                    </div>
                    <div class="field">
                      <label>Частота</label>
                      <select class="input select" v-model="habitEditForm.frequency">
                        <option value="daily">Ежедневно</option>
                        <option value="weekly">Еженедельно</option>
                        <option value="workdays">По будням</option>
                        <option value="custom">Другое</option>
                      </select>
                    </div>
                    <p v-if="habitEditError" class="error-msg">{{ habitEditError }}</p>
                    <div class="habit-delete-actions">
                      <button class="cancel-btn" @click="closeHabitEdit" :disabled="updatingHabit">Отмена</button>
                      <button class="comment-save-btn" @click="saveHabitEdit" :disabled="updatingHabit">
                        <span v-if="!updatingHabit">Сохранить</span>
                        <span v-else class="spinner"></span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="commentModal" class="habit-delete-modal-backdrop" @click.self="onCommentModalBackdrop">
                <div class="comment-modal" @click.stop>
                  <h4>Заметка к дню</h4>
                  <p class="comment-modal-sub">
                    <strong>{{ commentModal.habit.name }}</strong>
                    · {{ commentModal.day.day }} {{ currentMonthLabel }}
                  </p>
                  <textarea
                    v-model="commentDraft"
                    class="input comment-textarea"
                    rows="4"
                    placeholder="Например: сделал 20 минут, было тяжело…"
                    :disabled="commentSaving"
                  ></textarea>
                  <p v-if="commentModalError" class="error-msg">{{ commentModalError }}</p>
                  <p class="comment-modal-hint">Клик по ячейке по-прежнему меняет ✓ / ✕. Пустая заметка при отсутствии отметки удаляет запись дня.</p>
                  <div class="habit-delete-actions">
                    <button type="button" class="cancel-btn" @click="closeCommentModal" :disabled="commentSaving">Отмена</button>
                    <button type="button" class="comment-save-btn" @click="saveDayComment" :disabled="commentSaving">
                      <span v-if="!commentSaving">Сохранить</span>
                      <span v-else class="spinner"></span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- ── PROFILE PAGE ── -->
      <transition name="page-fade" mode="out-in">
        <div v-if="page === 'profile'" key="profile" class="page">
          <div class="profile-card">
            <div class="profile-avatar">{{ user.name[0].toUpperCase() }}</div>
            <div class="profile-meta">
              <h2 class="profile-name">{{ user.name }}</h2>
              <p class="profile-email">{{ user.email }}</p>
            </div>
          </div>

          <!-- Edit form -->
          <div class="section-card">
            <h3 class="section-title">Изменить данные</h3>
            <div class="edit-form">
              <div class="field-row">
                <div class="field">
                  <label>Имя</label>
                  <input class="input" v-model="editForm.name" placeholder="Имя"/>
                </div>
                <div class="field">
                  <label>Возраст</label>
                  <input class="input" type="number" v-model="editForm.age" placeholder="Возраст" min="1" max="120"/>
                </div>
              </div>
              <div class="field">
                <label>Email</label>
                <input class="input" type="email" v-model="editForm.email" placeholder="Email"/>
              </div>
              <div class="field">
                <label>Новый пароль <span class="optional">(оставьте пустым если не меняете)</span></label>
                <input class="input" type="password" v-model="editForm.newPassword" placeholder="••••••••"/>
              </div>
              <div class="field">
                <label>Текущий пароль <span class="required">*</span></label>
                <input class="input" type="password" v-model="editForm.currentPassword" placeholder="Для подтверждения изменений"/>
              </div>
              <p v-if="editError" class="error-msg">{{ editError }}</p>
              <p v-if="editSuccess" class="success-msg">{{ editSuccess }}</p>
              <button class="save-btn" @click="saveProfile" :disabled="savingProfile">
                <span v-if="!savingProfile">Сохранить изменения</span>
                <span v-else class="spinner"></span>
              </button>
            </div>
          </div>

          <!-- Danger zone -->
          <div class="section-card danger-card">
            <h3 class="section-title danger-title">Удаление аккаунта</h3>
            <p class="danger-desc">Это действие необратимо. Все привычки и данные будут удалены.</p>
            <div v-if="!showDeleteConfirm">
              <button class="danger-btn" @click="showDeleteConfirm = true">Удалить аккаунт</button>
            </div>
            <div v-else class="delete-confirm">
              <div class="field">
                <label>Введите пароль для подтверждения</label>
                <input class="input" type="password" v-model="deletePassword" placeholder="••••••••"/>
              </div>
              <p v-if="deleteError" class="error-msg">{{ deleteError }}</p>
              <div class="confirm-actions">
                <button class="cancel-btn" @click="showDeleteConfirm = false; deletePassword = ''">Отмена</button>
                <button class="danger-btn" @click="deleteAccount" :disabled="deletingAccount">
                  <span v-if="!deletingAccount">Подтвердить удаление</span>
                  <span v-else class="spinner"></span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <div v-if="showLogoutConfirm" class="habit-delete-modal-backdrop" @click.self="cancelLogout">
        <div class="habit-delete-modal">
          <h4>Выйти из аккаунта?</h4>
          <p>Вы сможете войти снова в любое время.</p>
          <div class="habit-delete-actions">
            <button class="cancel-btn" @click="cancelLogout">Отмена</button>
            <button class="danger-btn" @click="confirmLogout">Выйти</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
const API = 'http://127.0.0.1:8000';
const TOKEN_KEY = 'access_token';
const ax = () => {
  const token = localStorage.getItem(TOKEN_KEY);
  return axios.create({
    withCredentials: true,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
};

const MONTHS_RU = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
];
const FREQUENCY_GROUPS = [
  { key: 'daily', label: 'Ежедневно' },
  { key: 'weekly', label: 'Еженедельно' },
  { key: 'workdays', label: 'По будням' },
  { key: 'custom', label: 'Другое' },
];

function getMonthDays() {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const localDateKey = (date) => {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  };
  const todayKey = localDateKey(today);
  return Array.from({ length: daysInMonth }, (_, i) => {
    const d = new Date(year, month, i + 1);
    const localKey = localDateKey(d);
    const isToday = localKey === todayKey;
    return { key: i + 1, day: i + 1, date: localKey, isToday };
  });
}

export default {
  name: 'DashboardComponent',
  props: {
    user: Object,
    theme: { type: String, default: 'dark' },
  },
  emits: ['logout', 'toggleTheme'],
  data() {
    return {
      page: 'habits',
      sidebarOpen: false,
      habits: [],
      logs: [],        // all habit logs: { id, habit_id, date, status, comment }
      loadingHabits: false,
      addingHabit: false,
      newHabit: { name: '', frequency: 'daily' },
      monthDays: getMonthDays(),
      currentMonthLabel: `${MONTHS_RU[new Date().getMonth()]} ${new Date().getFullYear()}`,
      pendingDeleteHabit: null,
      deletingHabit: false,
      habitEditModal: null,
      habitEditForm: { name: '', frequency: 'daily' },
      habitEditError: '',
      updatingHabit: false,
      // profile
      editForm: { name: this.user.name, age: this.user.age || '', email: this.user.email, newPassword: '', currentPassword: '' },
      editError: '',
      editSuccess: '',
      savingProfile: false,
      showDeleteConfirm: false,
      deletePassword: '',
      deleteError: '',
      deletingAccount: false,
      commentModal: null,
      commentDraft: '',
      commentSaving: false,
      commentModalError: '',
      showLogoutConfirm: false,
    };
  },
  mounted() {
    this.loadHabits();
  },
  computed: {
    groupedHabits() {
      return FREQUENCY_GROUPS
        .map(group => ({
          ...group,
          items: this.habits.filter(h => h.frequency === group.key),
        }))
        .filter(group => group.items.length > 0);
    },
    todayKey() {
      const now = new Date();
      const y = now.getFullYear();
      const m = String(now.getMonth() + 1).padStart(2, '0');
      const d = String(now.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    },
    todayTotalCount() {
      return this.habits.length;
    },
    monthTotalCount() {
      if (!this.habits.length) return 0;
      const todayDay = new Date().getDate();
      return this.habits.length * todayDay;
    },
    todayDoneCount() {
      return this.habits.reduce((count, habit) => (
        this.logs.some(l => l.habit_id === habit.id && l.date === this.todayKey && l.status === 'done')
          ? count + 1
          : count
      ), 0);
    },
    monthDoneCount() {
      const now = new Date();
      const y = now.getFullYear();
      const m = now.getMonth();
      const lastIncludedDay = now.getDate();
      return this.logs.filter((l) => {
        if (l.status !== 'done') return false;
        const logDate = new Date(`${l.date}T00:00:00`);
        return logDate.getFullYear() === y && logDate.getMonth() === m && logDate.getDate() <= lastIncludedDay;
      }).length;
    },
    todayProgressPercent() {
      if (!this.todayTotalCount) return 0;
      return Math.round((this.todayDoneCount / this.todayTotalCount) * 100);
    },
    monthProgressPercent() {
      if (!this.monthTotalCount) return 0;
      return Math.min(100, Math.round((this.monthDoneCount / this.monthTotalCount) * 100));
    },
    todayProgressColor() {
      const hue = Math.round((this.todayProgressPercent / 100) * 120);
      return `hsl(${hue}, 85%, 55%)`;
    },
    monthProgressColor() {
      const hue = Math.round((this.monthProgressPercent / 100) * 120);
      return `hsl(${hue}, 85%, 55%)`;
    },
    progressRingRadius() {
      return 50;
    },
    progressRingCircumference() {
      return 2 * Math.PI * this.progressRingRadius;
    },
    progressRingOffset() {
      return this.progressRingCircumference * (1 - this.todayProgressPercent / 100);
    },
    monthProgressRingOffset() {
      return this.progressRingCircumference * (1 - this.monthProgressPercent / 100);
    },
  },
  methods: {
    /* ── Habits ── */
    async loadHabits() {
      this.loadingHabits = true;
      try {
        const { data } = await ax().get(`${API}/habits`);
        this.habits = data.filter(h => h.user_id === this.user.id);
        await this.loadLogs();
      } catch (e) { console.error(e); }
      finally { this.loadingHabits = false; }
    },

    async loadLogs() {
      try {
        const { data } = await ax().get(`${API}/habit_logs`);
        this.logs = data;
      } catch (e) { console.error(e); }
    },

    async addHabit() {
      if (!this.newHabit.name.trim()) return;
      this.addingHabit = true;
      try {
        const { data } = await ax().post(`${API}/habits`, {
          user_id: this.user.id,
          name: this.newHabit.name.trim(),
          frequency: this.newHabit.frequency,
        });
        this.habits.push(data);
        this.newHabit.name = '';
      } catch (e) { console.error(e); }
      finally { this.addingHabit = false; }
    },

    requestDeleteHabit(habit) {
      this.pendingDeleteHabit = habit;
    },
    openHabitEdit(habit) {
      this.habitEditModal = habit;
      this.habitEditError = '';
      this.habitEditForm = {
        name: habit.name || '',
        frequency: habit.frequency || 'daily',
      };
    },
    closeHabitEdit() {
      this.habitEditModal = null;
      this.habitEditError = '';
    },
    onHabitEditBackdrop() {
      if (this.updatingHabit) return;
      this.closeHabitEdit();
    },
    async saveHabitEdit() {
      if (!this.habitEditModal) return;
      const name = this.habitEditForm.name.trim();
      if (!name) {
        this.habitEditError = 'Введите название привычки';
        return;
      }
      this.updatingHabit = true;
      this.habitEditError = '';
      try {
        const { data } = await ax().put(`${API}/habits/${this.habitEditModal.id}`, {
          name,
          frequency: this.habitEditForm.frequency,
        });
        this.habits = this.habits.map(h => (h.id === data.id ? data : h));
        this.closeHabitEdit();
      } catch (e) {
        this.habitEditError = e.response?.data?.detail || 'Не удалось сохранить изменения';
      } finally {
        this.updatingHabit = false;
      }
    },
    requestLogout() {
      this.showLogoutConfirm = true;
    },
    cancelLogout() {
      this.showLogoutConfirm = false;
    },
    confirmLogout() {
      this.showLogoutConfirm = false;
      this.$emit('logout');
    },
    cancelHabitDelete() {
      this.pendingDeleteHabit = null;
    },
    async confirmHabitDelete() {
      if (!this.pendingDeleteHabit) return;
      this.deletingHabit = true;
      const deleted = await this.deleteHabit(this.pendingDeleteHabit.id);
      this.deletingHabit = false;
      if (deleted) this.pendingDeleteHabit = null;
    },
    async deleteHabit(id) {
      try {
        const habitLogs = this.logs.filter(l => l.habit_id === id);
        if (habitLogs.length) {
          await Promise.allSettled(
            habitLogs.map(log =>
              ax().delete(`${API}/habit_logs/${log.id}`, { params: { habit_id: id } })
            )
          );
        }
        await ax().delete(`${API}/habits/${id}`);
        this.habits = this.habits.filter(h => h.id !== id);
        this.logs = this.logs.filter(l => l.habit_id !== id);
        return true;
      } catch (e) {
        console.error(e);
        return false;
      }
    },

    /* ── Logs / month tracker ── */
    isDone(habitId, date) {
      return this.logs.some(l => l.habit_id === habitId && l.date === date && l.status === 'done');
    },
    hasDayComment(habitId, date) {
      const log = this.logs.find(l => l.habit_id === habitId && l.date === date);
      return !!(log && String(log.comment || '').trim());
    },
    openCommentModal(habit, day) {
      const existing = this.logs.find(l => l.habit_id === habit.id && l.date === day.date);
      this.commentModal = { habit, day };
      this.commentDraft = existing?.comment != null ? String(existing.comment) : '';
      this.commentModalError = '';
    },
    closeCommentModal() {
      this.commentModal = null;
      this.commentDraft = '';
      this.commentModalError = '';
    },
    onCommentModalBackdrop() {
      if (this.commentSaving) return;
      this.closeCommentModal();
    },
    async saveDayComment() {
      if (!this.commentModal) return;
      const { habit, day } = this.commentModal;
      const text = this.commentDraft.trim();
      this.commentSaving = true;
      this.commentModalError = '';
      try {
        const existing = this.logs.find(l => l.habit_id === habit.id && l.date === day.date);
        if (!existing) {
          if (!text) {
            this.closeCommentModal();
            return;
          }
          const { data } = await ax().post(`${API}/habit_logs`, {
            habit_id: habit.id,
            date: day.date,
            status: 'missed',
            comment: text,
          });
          this.logs.push(data);
          this.closeCommentModal();
          return;
        }
        if (String(existing.comment || '').trim() === text) {
          this.closeCommentModal();
          return;
        }
        await ax().delete(`${API}/habit_logs/${existing.id}`, { params: { habit_id: habit.id } });
        if (!text && existing.status === 'missed') {
          this.logs = this.logs.filter(l => l.id !== existing.id);
          this.closeCommentModal();
          return;
        }
        const { data } = await ax().post(`${API}/habit_logs`, {
          habit_id: habit.id,
          date: day.date,
          status: existing.status,
          comment: text,
        });
        this.logs = this.logs.filter(l => l.id !== existing.id);
        this.logs.push(data);
        this.closeCommentModal();
      } catch (e) {
        const d = e.response?.data?.detail;
        this.commentModalError = Array.isArray(d)
          ? d.map((x) => x.msg || JSON.stringify(x)).join(' ')
          : (d || 'Не удалось сохранить заметку');
      } finally {
        this.commentSaving = false;
      }
    },
    async toggleDay(habit, day) {
      const existing = this.logs.find(l => l.habit_id === habit.id && l.date === day.date);
      if (existing) {
        // toggle status
        const newStatus = existing.status === 'done' ? 'missed' : 'done';
        try {
          // delete old log and create new (no PATCH on habit_logs in backend)
          await ax().delete(`${API}/habit_logs/${existing.id}`, { params: { habit_id: habit.id } });
          const { data } = await ax().post(`${API}/habit_logs`, {
            habit_id: habit.id,
            date: day.date,
            status: newStatus,
            comment: existing.comment || '',
          });
          this.logs = this.logs.filter(l => l.id !== existing.id);
          this.logs.push(data);
        } catch (e) { console.error(e); }
      } else {
        try {
          const { data } = await ax().post(`${API}/habit_logs`, {
            habit_id: habit.id,
            date: day.date,
            status: 'done',
            comment: '',
          });
          this.logs.push(data);
        } catch (e) { console.error(e); }
      }
    },
    /* ── Profile ── */
    async saveProfile() {
      this.editError = '';
      this.editSuccess = '';
      if (!this.editForm.currentPassword) { this.editError = 'Введите текущий пароль'; return; }
      this.savingProfile = true;
      try {
        const payload = {
          name: this.editForm.name,
          age: Number(this.editForm.age),
          email: this.editForm.email,
        };
        if (this.editForm.newPassword) payload.password = this.editForm.newPassword;
        await ax().patch(`${API}/users/me`, payload, {
          params: { password: this.editForm.currentPassword },
        });
        this.editSuccess = 'Данные обновлены!';
        this.editForm.currentPassword = '';
        this.editForm.newPassword = '';
      } catch (e) {
        this.editError = e.response?.data?.detail || 'Ошибка при сохранении';
      } finally {
        this.savingProfile = false;
      }
    },

    async deleteAccount() {
      if (!this.deletePassword) { this.deleteError = 'Введите пароль'; return; }
      this.deleteError = '';
      this.deletingAccount = true;
      try {
        await ax().delete(`${API}/users/me`, {
          // Send password in both places to support different backend parsers.
          params: { password: this.deletePassword },
          data: { password: this.deletePassword },
        });
        localStorage.removeItem(TOKEN_KEY);
        this.$emit('logout');
      } catch (e) {
        this.deleteError = e.response?.data?.detail || 'Неверный пароль';
      } finally {
        this.deletingAccount = false;
      }
    },
  },
};
</script>

<style scoped>
/* ── Variables ── */
.dashboard.dark {
  --bg: #050508;
  --sidebar-bg: rgba(8,10,22,0.97);
  --card-bg: rgba(10,12,25,0.8);
  --border: rgba(79,142,247,0.15);
  --text: #ffffff;
  --text-sub: rgba(255,255,255,0.4);
  --text-label: rgba(255,255,255,0.35);
  --input-bg: rgba(255,255,255,0.04);
  --input-border: rgba(255,255,255,0.1);
  --nav-hover: rgba(79,142,247,0.08);
  --nav-active: rgba(79,142,247,0.15);
  --topbar-bg: rgba(5,5,8,0.9);
  --shadow: 0 8px 32px rgba(0,0,0,0.4);
  --day-bg: rgba(255,255,255,0.04);
  --day-border: rgba(255,255,255,0.08);
  --orb-opacity: 0.12;
}
.dashboard.light {
  --bg: #f0f4ff;
  --sidebar-bg: rgba(255,255,255,0.98);
  --card-bg: rgba(255,255,255,0.9);
  --border: rgba(79,142,247,0.2);
  --text: #0f1729;
  --text-sub: rgba(15,23,41,0.45);
  --text-label: rgba(15,23,41,0.5);
  --input-bg: rgba(79,142,247,0.04);
  --input-border: rgba(79,142,247,0.18);
  --nav-hover: rgba(79,142,247,0.06);
  --nav-active: rgba(79,142,247,0.12);
  --topbar-bg: rgba(240,244,255,0.95);
  --shadow: 0 8px 32px rgba(79,142,247,0.1);
  --day-bg: rgba(79,142,247,0.04);
  --day-border: rgba(79,142,247,0.15);
  --orb-opacity: 0.07;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard {
  display: flex;
  min-height: 100vh;
  background: var(--bg);
  font-family: 'DM Sans', sans-serif;
  position: relative;
  transition: background 0.4s;
}

.bg-orb {
  position: fixed; border-radius: 50%;
  filter: blur(100px); opacity: var(--orb-opacity);
  pointer-events: none; z-index: 0;
  transition: opacity 0.4s;
}
.orb-1 { width: 600px; height: 600px; background: radial-gradient(circle, #4f8ef7, transparent 70%); top: -200px; left: -200px; }
.orb-2 { width: 500px; height: 500px; background: radial-gradient(circle, #a855f7, transparent 70%); bottom: -150px; right: -150px; }

/* ── Sidebar ── */
.sidebar {
  width: 240px; flex-shrink: 0;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  padding: 24px 16px;
  position: sticky; top: 0; height: 100vh;
  z-index: 50;
  backdrop-filter: blur(20px);
  transition: background 0.4s, border-color 0.4s;
}
.sidebar-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 32px; padding: 0 8px;
}
.brand { display: flex; align-items: center; gap: 10px; }
.brand-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: rgba(79,142,247,0.1);
  border: 1px solid rgba(79,142,247,0.2);
  display: flex; align-items: center; justify-content: center;
}
.brand-name {
  font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 800;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sidebar-close {
  display: none; background: none; border: none;
  color: var(--text-sub); cursor: pointer; padding: 4px;
}

.sidebar-nav { flex: 1; display: flex; flex-direction: column; gap: 4px; }
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 10px; border: none;
  background: transparent; color: var(--text-sub);
  font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 500;
  cursor: pointer; text-align: left; width: 100%;
  transition: all 0.2s;
}
.nav-item:hover { background: var(--nav-hover); color: var(--text); }
.nav-item.active { background: var(--nav-active); color: #4f8ef7; }

.sidebar-footer { display: flex; flex-direction: column; gap: 4px; }
.theme-btn, .logout-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 10px; border: none;
  background: transparent;
  font-family: 'DM Sans', sans-serif; font-size: 14px; cursor: pointer;
  width: 100%; text-align: left; transition: all 0.2s;
}
.theme-btn { color: var(--text-sub); }
.theme-btn:hover { background: var(--nav-hover); color: var(--text); }
.logout-btn { color: #f87171; }
.logout-btn:hover { background: rgba(248,113,113,0.08); }

/* ── Overlay ── */
.overlay {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,0.5); z-index: 40;
  backdrop-filter: blur(2px);
}

/* ── Main ── */
.main {
  flex: 1; display: flex; flex-direction: column;
  min-height: 100vh; position: relative; z-index: 1;
  overflow-x: hidden;
}

/* Topbar */
.topbar {
  position: sticky; top: 0; z-index: 30;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(16px);
  padding: 0 24px; height: 60px;
  display: flex; align-items: center; gap: 16px;
  transition: background 0.4s, border-color 0.4s;
}
.burger {
  display: none; background: none; border: none;
  color: var(--text-sub); cursor: pointer; padding: 4px;
}
.topbar-title {
  flex: 1; font-family: 'Syne', sans-serif;
  font-size: 18px; font-weight: 700; color: var(--text);
}
.topbar-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700; color: #fff;
  cursor: pointer; transition: transform 0.2s;
  box-shadow: 0 0 20px rgba(79,142,247,0.3);
}
.topbar-avatar:hover { transform: scale(1.08); }

/* ── Page ── */
.page { padding: 28px 24px; max-width: 780px; }
.page.page-habits {
  max-width: 100%;
}

/* Add card */
.add-card, .section-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 20px; padding: 24px;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow);
  margin-bottom: 24px;
  transition: background 0.4s, border-color 0.4s;
}
.section-title {
  font-family: 'Syne', sans-serif;
  font-size: 15px; font-weight: 700; color: var(--text);
  margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}
.count-badge {
  background: rgba(79,142,247,0.15);
  color: #4f8ef7; font-size: 12px; font-weight: 600;
  padding: 2px 8px; border-radius: 20px;
  font-family: 'DM Sans', sans-serif;
}

.add-form { display: flex; gap: 10px; align-items: flex-end; }
.add-inputs { display: flex; gap: 10px; flex: 1; flex-wrap: wrap; }
.input {
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: 10px; padding: 11px 14px;
  color: var(--text); font-family: 'DM Sans', sans-serif;
  font-size: 14px; outline: none; width: 100%;
  transition: all 0.3s;
}
.input::placeholder { color: var(--text-sub); }
.input:focus { border-color: rgba(79,142,247,0.5); box-shadow: 0 0 0 3px rgba(79,142,247,0.1); }
.select {
  cursor: pointer;
  appearance: none;
  border-color: rgba(79,142,247,0.3);
  background:
    linear-gradient(135deg, rgba(79,142,247,0.1), rgba(168,85,247,0.06)),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%234f8ef7' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat, no-repeat;
  background-position: 0 0, right 12px center;
  background-size: auto, 12px 12px;
  padding-right: 34px;
  font-weight: 600;
}
.select:hover {
  border-color: rgba(79,142,247,0.45);
}
.select:focus {
  border-color: rgba(79,142,247,0.6);
  box-shadow: 0 0 0 3px rgba(79,142,247,0.14);
}
.select option {
  color: #0f1729;
  background: #ffffff;
}
.add-inputs .input:first-child { flex: 2; min-width: 160px; }
.add-inputs .input:last-child { flex: 1; min-width: 140px; }

.add-btn {
  padding: 11px 18px; border: none; border-radius: 10px;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  color: #fff; font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; gap: 6px;
  white-space: nowrap;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 16px rgba(79,142,247,0.3);
  flex-shrink: 0;
}
.add-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(79,142,247,0.4); }
.add-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* Habits list */
.habits-section { }
.habits-list { display: flex; flex-direction: column; gap: 12px; }
.habits-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 14px;
  align-items: start;
  width: 100%;
}
.habits-tables {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}
.month-title {
  font-family: 'Syne', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}
.frequency-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.frequency-title {
  font-family: 'Syne', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-sub);
}
.progress-cards {
  display: flex;
  gap: 12px;
  position: sticky;
  top: 74px;
  margin-top: 28px;
  align-self: start;
  justify-self: end;
}
.progress-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow);
  padding: 14px 12px;
  width: 188px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.progress-title {
  font-family: 'Syne', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
  text-align: center;
}
.progress-ring-wrap {
  position: relative;
  width: 122px;
  height: 122px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.progress-ring {
  width: 116px;
  height: 116px;
  transform: rotate(-90deg);
}
.progress-bg {
  fill: none;
  stroke: var(--day-border);
  stroke-width: 10;
}
.progress-value {
  fill: none;
  stroke-width: 10;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.35s ease, stroke 0.35s ease;
}
.progress-center {
  position: absolute;
  inset: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(79,142,247,0.06);
  border: 1px solid var(--border);
}
.progress-percent {
  font-family: 'Syne', sans-serif;
  font-size: 19px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.2px;
  font-variant-numeric: tabular-nums;
}
.progress-meta {
  color: var(--text-sub);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.15px;
}
.month-table-wrap {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow-x: auto;
  overflow-y: hidden;
  box-shadow: var(--shadow);
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.month-table-wrap::-webkit-scrollbar {
  width: 0;
  height: 0;
}
.month-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
}
.month-table th,
.month-table td {
  border-bottom: 1px solid var(--border);
}
.month-table tbody tr:last-child td {
  border-bottom: none;
}
.month-table tbody tr:last-child td:first-child {
  border-bottom-left-radius: 14px;
}
.month-table tbody tr:last-child td:last-child {
  border-bottom-right-radius: 14px;
}
.habit-col,
.day-col {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-sub);
  background: rgba(79,142,247,0.08);
  padding: 10px 8px;
  text-align: center;
}
.action-col {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-sub);
  background: rgba(79,142,247,0.08);
  padding: 10px 8px;
  text-align: center;
  min-width: 84px;
}
.habit-col {
  text-align: left;
  min-width: 240px;
}
.day-col.today {
  color: #4f8ef7;
}
.habit-cell {
  background: var(--card-bg);
  min-width: 240px;
}
.habit-cell-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  min-height: 52px;
}
.habit-main { min-width: 0; }
.edit-btn {
  background: rgba(79,142,247,0.12);
  border: 1px solid rgba(79,142,247,0.35);
  color: #4f8ef7;
  border-radius: 8px;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}
.edit-btn:hover {
  background: rgba(79,142,247,0.2);
  transform: translateY(-1px);
}
.action-cell {
  width: 84px;
  min-width: 84px;
  text-align: center;
  background: var(--card-bg);
}
.status-cell {
  position: relative;
  width: 38px;
  min-width: 38px;
  text-align: center;
  font-size: 15px;
  font-weight: 700;
  color: #f87171;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s, color 0.2s;
  vertical-align: middle;
}
.status-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 2px 14px 10px 2px;
}
.comment-chip {
  position: absolute;
  bottom: 3px;
  right: 2px;
  width: 16px;
  height: 16px;
  padding: 0;
  border: none;
  border-radius: 5px;
  background: rgba(79,142,247,0.12);
  color: var(--text-sub);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 0;
  transition: background 0.2s, color 0.2s, transform 0.15s;
  z-index: 2;
}
.comment-chip:hover {
  background: rgba(79,142,247,0.22);
  color: #4f8ef7;
  transform: scale(1.06);
}
.comment-chip.active {
  background: rgba(79,142,247,0.28);
  color: #4f8ef7;
}
.status-cell.has-comment:not(.done) .comment-chip {
  color: #4f8ef7;
}
.status-cell:hover {
  background: rgba(79,142,247,0.08);
}
.status-cell.done {
  color: #4ade80;
}
.status-cell.today {
  background: rgba(79,142,247,0.08);
}

.loading-state, .empty-state {
  padding: 48px; text-align: center;
  color: var(--text-sub); font-size: 14px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
}

.habit-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.delete-btn {
  background: none; border: none; cursor: pointer;
  color: var(--text-sub); padding: 6px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
  margin: 0 auto;
}
.delete-btn:hover { color: #f87171; background: rgba(248,113,113,0.1); }
.delete-btn.solid {
  background: rgba(248,113,113,0.12);
  border: 1px solid rgba(248,113,113,0.35);
  color: #f87171;
}

.habit-delete-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 120;
  padding: 16px;
}
.habit-delete-modal {
  width: min(440px, 100%);
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow);
  padding: 18px;
}
.habit-delete-modal h4 {
  font-family: 'Syne', sans-serif;
  font-size: 18px;
  color: var(--text);
  margin-bottom: 10px;
}
.habit-delete-modal p {
  color: var(--text-sub);
  font-size: 14px;
  margin-bottom: 16px;
}
.comment-modal {
  width: min(440px, 100%);
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow);
  padding: 18px;
}
.comment-modal h4 {
  font-family: 'Syne', sans-serif;
  font-size: 18px;
  color: var(--text);
  margin-bottom: 8px;
}
.comment-modal-sub {
  color: var(--text-sub);
  font-size: 14px;
  margin-bottom: 14px;
  line-height: 1.45;
}
.comment-modal-sub strong {
  color: var(--text);
  font-weight: 600;
}
.comment-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: 'DM Sans', sans-serif;
  line-height: 1.45;
  margin-bottom: 10px;
}
.comment-modal-hint {
  font-size: 12px;
  color: var(--text-sub);
  line-height: 1.4;
  margin-bottom: 14px;
  margin-top: -4px;
}
.comment-save-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  -webkit-appearance: none;
  appearance: none;
  background-color: #5b6ef5;
  background-image: linear-gradient(135deg, #4f8ef7 0%, #9333ea 100%);
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, filter 0.2s;
  box-shadow: 0 4px 14px rgba(79,142,247,0.45);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  opacity: 1;
}
.comment-save-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(79,142,247,0.55);
  filter: brightness(1.03);
}
.comment-save-btn:disabled {
  opacity: 0.85;
  cursor: not-allowed;
  filter: grayscale(0.08) brightness(0.95);
}
.comment-save-btn .spinner {
  border-color: rgba(255,255,255,0.35);
  border-top-color: #fff;
}
.habit-delete-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ── Profile page ── */
.profile-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 20px; padding: 28px 24px;
  display: flex; align-items: center; gap: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(16px);
  transition: background 0.4s, border-color 0.4s;
}
.profile-avatar {
  width: 64px; height: 64px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 700; color: #fff;
  box-shadow: 0 0 30px rgba(79,142,247,0.3);
}
.profile-name { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; color: var(--text); }
.profile-email { font-size: 14px; color: var(--text-sub); margin-top: 2px; }

.edit-form { display: flex; flex-direction: column; gap: 16px; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.6px; color: var(--text-label);
}
.optional { font-size: 10px; text-transform: none; letter-spacing: 0; color: var(--text-sub); font-weight: 400; }
.required { color: #f87171; }

.save-btn {
  padding: 12px; border: none; border-radius: 12px;
  background: linear-gradient(135deg, #4f8ef7, #a855f7);
  color: #fff; font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 16px rgba(79,142,247,0.3);
  margin-top: 4px;
}
.save-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(79,142,247,0.4); }
.save-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* Danger zone */
.danger-card { border-color: rgba(248,113,113,0.2); }
.danger-title { color: #f87171; }
.danger-desc { font-size: 13px; color: var(--text-sub); margin-bottom: 16px; margin-top: -8px; }
.danger-btn {
  padding: 10px 20px; border: 1px solid rgba(248,113,113,0.4);
  border-radius: 10px; background: rgba(248,113,113,0.08);
  color: #f87171; font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500; cursor: pointer;
  transition: all 0.2s;
}
.danger-btn:hover:not(:disabled) { background: rgba(248,113,113,0.15); border-color: rgba(248,113,113,0.6); }
.danger-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.delete-confirm { display: flex; flex-direction: column; gap: 12px; }
.confirm-actions { display: flex; gap: 10px; }
.cancel-btn {
  padding: 10px 20px; border: 1px solid var(--border);
  border-radius: 10px; background: var(--input-bg);
  color: var(--text-sub); font-family: 'DM Sans', sans-serif;
  font-size: 14px; cursor: pointer; transition: all 0.2s;
}
.cancel-btn:hover { color: var(--text); }

/* Messages */
.error-msg {
  color: #f87171; font-size: 13px;
  padding: 10px 12px;
  background: rgba(248,113,113,0.08);
  border: 1px solid rgba(248,113,113,0.2);
  border-radius: 8px; animation: shake 0.4s ease;
}
@keyframes shake {
  0%,100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
.success-msg {
  color: #4ade80; font-size: 13px;
  padding: 10px 12px;
  background: rgba(74,222,128,0.08);
  border: 1px solid rgba(74,222,128,0.2);
  border-radius: 8px;
}

/* Spinner */
.spinner {
  display: inline-block; width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff;
  border-radius: 50%; animation: spin 0.7s linear infinite; vertical-align: middle;
}
.spinner.big { width: 32px; height: 32px; border-width: 3px; border-top-color: #4f8ef7; border-color: var(--input-border); border-top-color: #4f8ef7; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Page transitions */
.page-fade-enter-active { transition: all 0.3s ease; }
.page-fade-leave-active { transition: all 0.2s ease; }
.page-fade-enter-from { opacity: 0; transform: translateY(12px); }
.page-fade-leave-to { opacity: 0; transform: translateY(-8px); }

/* Habit list transitions */
.habit-item-enter-active { transition: all 0.35s cubic-bezier(0.34,1.2,0.64,1); }
.habit-item-leave-active { transition: all 0.2s ease; }
.habit-item-enter-from { opacity: 0; transform: translateY(16px); }
.habit-item-leave-to { opacity: 0; transform: translateX(-16px); }

/* ── Mobile ── */
@media (max-width: 768px) {
  .sidebar {
    position: fixed; left: -260px; top: 0; height: 100vh;
    width: 240px;
    transition: left 0.3s cubic-bezier(0.34,1.2,0.64,1);
    box-shadow: none;
  }
  .sidebar.open { left: 0; box-shadow: 4px 0 40px rgba(0,0,0,0.3); }
  .sidebar-close { display: flex; }
  .overlay { display: block; }
  .burger { display: flex; }
  .main { width: 100%; }
  .page { padding: 20px 16px; }
  .add-form { flex-direction: column; }
  .add-btn { width: 100%; justify-content: center; }
  .habit-col,
  .habit-cell {
    min-width: 180px;
  }
  .month-table {
    min-width: 760px;
  }
  .habits-layout {
    grid-template-columns: 1fr;
  }
  .progress-cards {
    position: static;
    margin-top: 0;
    width: 100%;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
  }
  .progress-card {
    width: min(260px, 100%);
    flex-direction: row;
    justify-content: center;
    gap: 14px;
  }
  .progress-title {
    display: none;
  }
  .progress-ring-wrap {
    width: 88px;
    height: 88px;
  }
  .progress-ring {
    width: 84px;
    height: 84px;
  }
  .progress-percent {
    font-size: 15px;
  }
  .field-row { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .topbar { padding: 0 16px; }
  .profile-card { flex-direction: column; text-align: center; }
}
</style>