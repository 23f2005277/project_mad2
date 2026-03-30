<!---<script setup>

</script>

<template>
    <div>
    <RouterLink to="/admin"> Admin View</RouterLink>
    <RouterLink to="/patient"> Patient View</RouterLink>
    <RouterLink to="/doctor"> Doctor View</RouterLink>
    </div>
</template> -->

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="home">
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <div class="content">
      <div class="badge">Healthcare Portal</div>
      <h1 class="title">
        Your Health,<br/>
        <span class="accent">Our Priority</span>
      </h1>
      <p class="subtitle">
        A unified platform connecting patients and doctors for seamless healthcare management.
      </p>

      <div class="actions">
        <RouterLink to="/login" class="btn btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
          Log In
        </RouterLink>
        <RouterLink to="/register" class="btn btn-outline">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
          Register as Patient
        </RouterLink>
      </div>

      <p class="note">Are you a doctor? Contact your admin to get access.</p>
    </div>

    <div class="card-grid">
      <div class="info-card">
        <div class="card-icon">🩺</div>
        <h3>For Doctors</h3>
        <p>Pre-registered by admin. Log in to manage your patients.</p>
      </div>
      <div class="info-card highlighted">
        <div class="card-icon">🏥</div>
        <h3>For Patients</h3>
        <p>Register yourself and get connected with your doctor.</p>
      </div>
      <div class="info-card">
        <div class="card-icon">🔐</div>
        <h3>For Admins</h3>
        <p>Manage doctors, patients, and system access securely.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,600;1,300&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.home {
  min-height: 100vh;
  background: #f0ebe3;
  font-family: 'DM Sans', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  position: relative;
  overflow: hidden;
}

/* Background shapes */
.bg-shapes { position: absolute; inset: 0; pointer-events: none; }

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.35;
}
.shape-1 {
  width: 500px; height: 500px;
  background: #c8d8b0;
  top: -150px; right: -100px;
  animation: drift 8s ease-in-out infinite alternate;
}
.shape-2 {
  width: 350px; height: 350px;
  background: #b8cce4;
  bottom: -100px; left: -80px;
  animation: drift 10s ease-in-out infinite alternate-reverse;
}
.shape-3 {
  width: 200px; height: 200px;
  background: #e4c8b0;
  top: 40%; left: 50%;
  animation: drift 12s ease-in-out infinite alternate;
}

@keyframes drift {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(30px, 20px) scale(1.05); }
}

/* Content */
.content {
  position: relative;
  text-align: center;
  max-width: 620px;
  animation: fadeUp 0.8s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.badge {
  display: inline-block;
  background: #2d5a3d;
  color: #e8f5ee;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0.35rem 0.9rem;
  border-radius: 100px;
  margin-bottom: 1.5rem;
}

.title {
  font-family: 'Fraunces', serif;
  font-size: clamp(2.8rem, 7vw, 4.5rem);
  font-weight: 300;
  line-height: 1.1;
  color: #1a2e1f;
  margin-bottom: 1.2rem;
}

.accent {
  font-style: italic;
  color: #2d5a3d;
}

.subtitle {
  font-size: 1.05rem;
  color: #5a6b5e;
  line-height: 1.7;
  max-width: 480px;
  margin: 0 auto 2.5rem;
  font-weight: 300;
}

/* Buttons */
.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.8rem;
  border-radius: 100px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.22s ease;
  cursor: pointer;
}

.btn-primary {
  background: #2d5a3d;
  color: #fff;
  box-shadow: 0 4px 20px rgba(45, 90, 61, 0.25);
}
.btn-primary:hover {
  background: #1a3d28;
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(45, 90, 61, 0.35);
}

.btn-outline {
  background: transparent;
  color: #2d5a3d;
  border: 1.5px solid #2d5a3d;
}
.btn-outline:hover {
  background: #2d5a3d;
  color: #fff;
  transform: translateY(-2px);
}

.note {
  font-size: 0.82rem;
  color: #8a9e8e;
  margin-top: 0.5rem;
}

/* Info cards */
.card-grid {
  display: flex;
  gap: 1rem;
  margin-top: 4rem;
  flex-wrap: wrap;
  justify-content: center;
  position: relative;
  animation: fadeUp 0.8s 0.2s ease both;
}

.info-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.8);
  border-radius: 16px;
  padding: 1.5rem 1.4rem;
  width: 180px;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(45, 90, 61, 0.12);
}

.info-card.highlighted {
  background: rgba(45, 90, 61, 0.08);
  border-color: rgba(45, 90, 61, 0.2);
}

.card-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }

.info-card h3 {
  font-family: 'Fraunces', serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1a2e1f;
  margin-bottom: 0.4rem;
}

.info-card p {
  font-size: 0.78rem;
  color: #6b7f6e;
  line-height: 1.5;
}
</style>