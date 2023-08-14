import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

import Project from '../views/Project.vue'
import Person from '../views/Person.vue'
import Facility from '../views/Facility.vue'
import Contact from '../views/Contact.vue'
import Privacy from '../views/Privacy.vue'
import Download from '../views/Download.vue'
import Search from '../views/Search.vue'
import AllProjects from '../views/AllProjects.vue'
import Explore from '../views/Explore.vue'
import ContactSuccess from '../views/ContactSuccess.vue'
import ExploreResults from '../views/ExploreResults.vue'
import PageNotFound from '../views/PageNotFound.vue'
import MapPage from '../views/Map.vue'
import Cookies from '../views/Cookies.vue'
import Glossary from '../views/Glossary.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/admin',
    name: 'admin',
    component: Admin,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: Search,
  },
  {
    path: '/contact',
    name: 'contact',
    component: Contact,
  },
  {
    path: '/contact/success',
    name: 'contactSuccess',
    component: ContactSuccess,
  },
  {
    path: '/privacy-terms',
    name: 'privacy',
    component: Privacy,
  },
  {
    path: '/cookies',
    name: 'cookies',
    component: Cookies,
  },
  {
    path: '/taxonomy',
    name: 'glossary',
    component: Glossary,
  },
  {
    path: '/cookies',
    name: 'cookies',
    component: Cookies,
  },
  // {
  //   path: '/all-datasets',
  //   name: 'alldatasets',
  //   component: AllProjects,
  // },
  {
    path: '/explore',
    name: 'explore',
    component: Explore,
  },
  {
    path: '/explore-results',
    name: 'exploreResults',
    component: ExploreResults,
  },
  {
    path: '/facility/:facility_slug',
    name: 'facility',
    component: Facility,
  },
  {
    path: '/datasets/:project_id',
    name: 'dataset',
    component: Project,
  },
  {
    path: '/datasets/:project_id/download',
    name: 'download',
    component: Download,
  },
  {
    path: '/people/:person_slug',
    name: 'person',
    component: Person,
  },
  {
    // Default webpage: Page not found
    path: '/:pathMatch(.*)*',
    component: PageNotFound,
  },
  {
    path: '/world-map',
    component: MapPage,
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    document.getElementById('app').scrollIntoView({ behavior: 'smooth' });
  }
})

export default router
