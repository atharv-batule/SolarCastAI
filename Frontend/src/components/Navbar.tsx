import { Link, useLocation } from "react-router-dom";
import { Sun, BarChart3, LineChart, Lightbulb, LayoutDashboard } from "lucide-react";

const navItems = [
  { path: "/", label: "Home", icon: Sun },
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { path: "/forecast", label: "Forecast", icon: LineChart },
  { path: "/analytics", label: "Analytics", icon: BarChart3 },
];

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 glass-card border-b border-border/50">
      <div className="container mx-auto flex items-center justify-between h-16 px-4">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg solar-gradient flex items-center justify-center">
            <Sun className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="font-display font-bold text-lg text-foreground">
            SunCast <span className="text-gradient-solar">AI</span>
          </span>
        </Link>
        <div className="hidden md:flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-accent text-accent-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                }`}
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </Link>
            );
          })}
        </div>
        <div className="md:hidden flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`p-2 rounded-lg transition-all ${
                  isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground"
                }`}
              >
                <item.icon className="w-5 h-5" />
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
