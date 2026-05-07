<script setup lang="ts">
import { computed } from 'vue'
import { NTag } from 'naive-ui'

const props = defineProps<{
  label: string
  color: string
}>()

function parseHex(hex: string): { r: number; g: number; b: number } | null {
  const m = /^#([0-9a-fA-F]{6})$/.exec(hex.trim())
  if (!m?.[1]) return null
  const n = parseInt(m[1], 16)
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 }
}

function rgba(hex: string, alpha: number): string {
  const rgb = parseHex(hex)
  if (!rgb) return `rgba(107, 114, 128, ${alpha})`
  return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`
}

const tagColor = computed(() => {
  const c = props.color
  return {
    color: rgba(c, 0.14),
    textColor: c,
    borderColor: rgba(c, 0.26),
  }
})
</script>

<template>
  <n-tag size="small" round bordered :color="tagColor">
    {{ props.label }}
  </n-tag>
</template>
