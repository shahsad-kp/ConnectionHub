import './App.css'
import {Suspense} from "react";
import {AppRoutes} from "./routes";
import {axiosAuthorized} from "./services/axiosConfig.ts";

axiosAuthorized
function App() {
    return (
        <Suspense>
            <AppRoutes/>
        </Suspense>
    )
}

export default App
