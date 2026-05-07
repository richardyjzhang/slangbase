<script setup lang="ts">
import { NCard, NEmpty } from 'naive-ui'

defineProps<{
  description?: string
}>()
</script>

<template>
  <n-card>
    <n-empty :description="description ?? '页面占位 · 内容待开发'" />
  </n-card>
</template>
