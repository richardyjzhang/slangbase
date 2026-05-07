<script setup lang="ts">
import { computed, h, ref, type Component } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { NIcon, NLayout, NLayoutContent, NLayoutHeader, NLayoutSider, NMenu, type MenuOption } from 'naive-ui'
import {
  BookOutline,
  ChatbubblesOutline,
  GitNetworkOutline,
  GridOutline,
  LinkOutline,
  PeopleOutline,
  PricetagOutline,
  RocketOutline,
  SettingsOutline,
} from '@vicons/ionicons5'

const route = useRoute()
const collapsed = ref(false)

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions = computed<MenuOption[]>(() => [
  {
    label: () => h(RouterLink, { to: '/dashboard' }, { default: () => '仪表盘' }),
    key: '/dashboard',
    icon: renderIcon(GridOutline),
  },
  {
    label: '术语管理',
    key: 'terms',
    icon: renderIcon(BookOutline),
    children: [
      {
        label: () => h(RouterLink, { to: '/terms/dictionary' }, { default: () => '术语字典' }),
        key: '/terms/dictionary',
        icon: renderIcon(ChatbubblesOutline),
      },
      {
        label: () => h(RouterLink, { to: '/terms/graph' }, { default: () => '知识图谱' }),
        key: '/terms/graph',
        icon: renderIcon(GitNetworkOutline),
      },
      {
        label: () => h(RouterLink, { to: '/terms/release' }, { default: () => '发版管理' }),
        key: '/terms/release',
        icon: renderIcon(RocketOutline),
      },
    ],
  },
  {
    label: '系统配置',
    key: 'settings',
    icon: renderIcon(SettingsOutline),
    children: [
      {
        label: () => h(RouterLink, { to: '/settings/tags' }, { default: () => '标签管理' }),
        key: '/settings/tags',
        icon: renderIcon(PricetagOutline),
      },
      {
        label: () =>
          h(RouterLink, { to: '/settings/relation-types' }, { default: () => '关系类型' }),
        key: '/settings/relation-types',
        icon: renderIcon(LinkOutline),
      },
      {
        label: () => h(RouterLink, { to: '/settings/users' }, { default: () => '用户管理' }),
        key: '/settings/users',
        icon: renderIcon(PeopleOutline),
      },
      {
        label: () =>
          h(RouterLink, { to: '/settings/preferences' }, { default: () => '个性化设置' }),
        key: '/settings/preferences',
        icon: renderIcon(SettingsOutline),
      },
    ],
  },
])

const activeKey = computed(() => route.path)
const pageTitle = computed(() => (route.meta.title as string | undefined) ?? '')
</script>

<template>
  <n-layout class="h-screen">
    <n-layout-header bordered class="flex h-14 items-center px-6">
      <div class="flex flex-1 items-center gap-3">
        <span class="text-xl font-semibold tracking-wide">SlangBase</span>
        <span class="text-xs text-gray-400">行业黑话管理工具</span>
      </div>
      <span class="text-xs text-gray-400">登录待接入后端</span>
    </n-layout-header>
    <n-layout has-sider class="!h-[calc(100vh-3.5rem)]">
      <n-layout-sider
        v-model:collapsed="collapsed"
        bordered
        :width="220"
        :collapsed-width="64"
        collapse-mode="width"
        show-trigger
      >
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="20"
          :options="menuOptions"
          :value="activeKey"
          :default-expand-all="true"
        />
      </n-layout-sider>
      <n-layout-content class="bg-gray-50">
        <div class="px-6 py-5">
          <h2 v-if="pageTitle" class="mb-4 text-lg font-semibold text-gray-700">
            {{ pageTitle }}
          </h2>
          <RouterView />
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>
