import axios from "axios";
import {backendVersion, baseUrl} from "./apiEndpoints.ts";


const createAxiosInstance = (includeInterceptor: boolean = true) => {
    console.log(baseUrl, 'testing')
    const axiosInstance = axios.create({
        baseURL: `${baseUrl}/api/${backendVersion}`,
    });

    if (includeInterceptor) {
        axiosInstance.interceptors.request.use((config) => {
            const accessToken = localStorage.getItem('accessToken');
            if (accessToken) {
                config.headers['Authorization'] = `Bearer ${accessToken}`;
            }
            return config;
        });

        axiosInstance.interceptors.response.use(
            (response) => response,
            async (error) => {
                if (error.response && error.response.status === 401) {
                    const originalRequest = error.config;

                    if (!originalRequest._retry) {
                        originalRequest._retry = true;

                        try {
                            const newAccessToken = await refreshToken();
                            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                            return axiosInstance(originalRequest);
                        } catch (refreshError) {
                            return Promise.reject(refreshError);
                        }
                    }
                }

                return Promise.reject(error);
            }
        );
    }

    return axiosInstance;
};

const axiosAuthorized = createAxiosInstance(true); // With interceptor
const axiosInstance = createAxiosInstance(false); // Without interceptor

const refreshToken = async () => {
    try{
        const res = await axiosInstance.post(
            'auth/token/refresh/',
            {
                refresh: localStorage.getItem('refreshToken')
            }
        )
        const {access} = res.data;
        localStorage.setItem('accessToken', access);
        return access
    }
    catch (e) {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        return Promise.reject(e);
    }
}
export {axiosAuthorized, axiosInstance, refreshToken};