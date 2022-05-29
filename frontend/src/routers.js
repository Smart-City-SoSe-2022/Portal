import {createRouter, createWebHistory} from "vue-router";
import MessageSend from "@/components/MessageSend";
import CreateAccount from "@/components/CreateAccount";
import LandingPage from "@/components/LandingPage";
import LoginPage from "@/components/LoginPage";

const routes = [
    {
        path: '/',
        name: 'landingPage',
        component: LandingPage
    },
    {
        path: '/message',
        name: 'messageSend',
        component: MessageSend
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
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;
