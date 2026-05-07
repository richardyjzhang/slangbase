<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NTabPane, NTabs } from 'naive-ui'
import TagTypesPanel from './tags/TagTypesPanel.vue'
import TagsPanel from './tags/TagsPanel.vue'

const activeTab = ref<'tags' | 'tag-types'>('tags')
</script>

<template>
  <n-card>
    <n-tabs v-model:value="activeTab" type="line" animated>
      <n-tab-pane name="tags" tab="标签管理">
        <TagsPanel />
      </n-tab-pane>
      <n-tab-pane name="tag-types" tab="标签类型">
        <TagTypesPanel />
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>
