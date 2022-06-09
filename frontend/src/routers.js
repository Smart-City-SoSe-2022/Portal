import {createRouter, createWebHistory} from "vue-router";
import CreateAccount from "@/components/CreateAccount";
import LandingPage from "@/components/LandingPage";
import LoginPage from "@/components/LoginPage";
import accountDetails from "@/components/AccountDetails";

const routes = [
    {
        path: '/',
        name: 'landingPage',
        component: LandingPage
    },
    {
        path: '/login',
        name: 'loginPage',
        component: LoginPage
    },
    {
        path: '/create',
        name: 'createAccount',
        component: CreateAccount
    },
    {
        path: '/details',
        name: 'accountDetails',
        component: accountDetails
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;
