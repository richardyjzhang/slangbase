<script setup lang="ts">
import { ref } from 'vue'
import { NButton, NCard, NForm, NFormItem, NIcon, NInput, useMessage } from 'naive-ui'
import { LanguageOutline } from '@vicons/ionicons5'

const message = useMessage()

const formValue = ref({
  username: '',
  password: '',
})
const loading = ref(false)

async function handleLogin() {
  if (!formValue.value.username || !formValue.value.password) {
    message.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  await new Promise((r) => setTimeout(r, 200))
  loading.value = false
  message.info('登录逻辑待后端接入，当前页面仅为占位')
}
</script>

<template>
  <div
    class="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 to-slate-200"
  >
    <n-card class="w-[400px] shadow-lg">
      <div class="mb-6 flex flex-col items-center">
        <n-icon size="48" class="mb-2 text-blue-500">
          <LanguageOutline />
        </n-icon>
        <h1 class="text-2xl font-semibold tracking-wide">SlangBase</h1>
        <p class="mt-1 text-sm text-gray-500">行业黑话管理工具</p>
      </div>
      <n-form @submit.prevent>
        <n-form-item label="用户名">
          <n-input v-model:value="formValue.username" placeholder="请输入用户名" clearable />
        </n-form-item>
        <n-form-item label="密码">
          <n-input
            v-model:value="formValue.password"
            type="password"
            show-password-on="click"
            placeholder="请输入密码"
            @keyup.enter="handleLogin"
          />
        </n-form-item>
        <n-button type="primary" block :loading="loading" @click="handleLogin">登录</n-button>
      </n-form>
    </n-card>
  </div>
</template>
