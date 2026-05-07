<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NTabPane, NTabs } from 'naive-ui'
import PageStub from '@/components/PageStub.vue'
import TagTypesPanel from './tags/TagTypesPanel.vue'

const activeTab = ref<'tags' | 'tag-types'>('tag-types')
</script>

<template>
  <n-card>
    <n-tabs v-model:value="activeTab" type="line" animated>
      <n-tab-pane name="tags" tab="标签管理">
        <PageStub description="标签管理待开发，先去把标签类型建好吧。" />
      </n-tab-pane>
      <n-tab-pane name="tag-types" tab="标签类型">
        <TagTypesPanel />
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>
