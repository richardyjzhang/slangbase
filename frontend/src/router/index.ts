import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: '登录' },
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/views/DashboardView.vue'),
          meta: { title: '仪表盘' },
        },
        {
          path: 'terms/dictionary',
          name: 'terms-dictionary',
          component: () => import('@/views/terms/DictionaryView.vue'),
          meta: { title: '术语字典' },
        },
        {
          path: 'terms/graph',
          name: 'terms-graph',
          component: () => import('@/views/terms/GraphView.vue'),
          meta: { title: '知识图谱' },
        },
        {
          path: 'terms/release',
          name: 'terms-release',
          component: () => import('@/views/terms/ReleaseView.vue'),
          meta: { title: '发版管理' },
        },
        {
          path: 'settings/tags',
          name: 'settings-tags',
          component: () => import('@/views/settings/TagsView.vue'),
          meta: { title: '标签管理' },
        },
        {
          path: 'settings/relation-types',
          name: 'settings-relation-types',
          component: () => import('@/views/settings/RelationTypesView.vue'),
          meta: { title: '关系类型' },
        },
        {
          path: 'settings/users',
          name: 'settings-users',
          component: () => import('@/views/settings/UsersView.vue'),
          meta: { title: '用户管理' },
        },
        {
          path: 'settings/preferences',
          name: 'settings-preferences',
          component: () => import('@/views/settings/PreferencesView.vue'),
          meta: { title: '个性化设置' },
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

export default router
