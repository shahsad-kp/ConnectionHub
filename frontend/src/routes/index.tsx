import {PublicRoutes} from "./PublicRoutes.tsx";
import {PrivateRoutes} from "./PrivateRoutes.tsx";

export const AppRoutes = () => {
    return (
        <>
            <PublicRoutes/>
            <PrivateRoutes/>
        </>
    );
};