import { useEffect, useState } from "react";
import { Link, NavLink, Outlet } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import Logo from "../components/Logo.jsx";
import Avatar from "../components/Avatar.jsx";
import { LogoutButton } from "../auth/AuthButtons.jsx";
import { useData } from "../data/useData.js";

import {
    FolderIcon,
    GalleryIcon,
    UserIcon,
    UsersIcon,
    StarIcon,
} from '../components/Icons.jsx'



import './AppLayout.css';



const NAV_ITEMS = [
    { to: '/radna-okolina', label: 'Radna okolina', icon: <FolderIcon /> },
    { to: '/artic', label: 'Artic', icon: <GalleryIcon /> },
    { to: '/profil', label: 'Moj profil', icon: <UserIcon /> },
    { to: '/korisnici', label: 'Korisnici', icon: <UsersIcon /> },
    { to: '/favoriti', label: 'Favoriti', icon: <StarIcon /> },
];

export default function AppLayout() {
    const { user } = useAuth0();
    const data = useData();
    const [profile, setProfile] = useState(null);

    // Ime i slika iz našeg profila (/api/users/me), da se izmjene profila odmah vide
    // i ovdje. Dok se profil ne učita (ili ako dohvat ne uspije), koriste se podaci s Auth0.
    useEffect(() => {
        let cancelled = false;
        data.getMe()
            .then((me) => !cancelled && setProfile(me))
            .catch(() => {});
        return () => {
            cancelled = true;
        };
        // data.version se mijenja nakon svake izmjene
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [data.version]);

    const name = profile?.display_name || user?.name || user?.email || 'Korisnik';
    const picture = profile ? profile.avatar_url : user?.picture;

    return (
        <div className="shell">
            <header className="topbar">
                <Link to="/radna-okolina" className="topbar-home" aria-label="Imagic, pocetna">
                    <Logo />
                </Link>
                <div className="topbar__user">
                    <Avatar key={picture} user={{ name, email: user?.email, picture }} />
                    <span className="topbar__name">{name}</span>
                    <LogoutButton className="btn btn--ghost btn--sm" />
                </div>
            </header>

            <nav className="mainnav" aria-label="Glavna navigacija">
                {NAV_ITEMS.map(item => (
                    <NavLink key={item.to} to={item.to} className="mainnav__link">
                        {item.icon}
                        <span className="mainnav__label">{item.label}</span>
                    </NavLink>
                ))}
            </nav>
            <main className="shell__main">
                <Outlet />
            </main>
        </div>
    );
}
