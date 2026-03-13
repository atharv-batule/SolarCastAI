import { motion } from "framer-motion";
import { TrendingUp, Droplets, Sun, Clock, Battery, BarChart3 } from "lucide-react";

interface InsightCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  detail: string;
  index: number;
}

const InsightCard = ({ icon: Icon, title, description, detail, index }: InsightCardProps) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: index * 0.1 }}
    className="glass-card rounded-xl p-6"
  >
    <div className="flex items-start gap-4">
      <div className="w-12 h-12 rounded-lg bg-accent flex items-center justify-center flex-shrink-0">
        <Icon className="w-6 h-6 text-accent-foreground" />
      </div>
      <div>
        <h3 className="font-display font-semibold text-foreground">{title}</h3>
        <p className="text-sm text-muted-foreground mt-1">{description}</p>
        <div className="mt-3 bg-muted rounded-lg p-3">
          <p className="text-xs text-foreground font-medium">{detail}</p>
        </div>
      </div>
    </div>
  </motion.div>
);

const insightsData = [
  {
    icon: Clock,
    title: "Best Solar Generation Hours",
    description: "Historical analysis shows consistent peak generation between 10 AM and 2 PM across all seasons.",
    detail: "Average peak output: 10.2 MW during optimal hours. Morning ramp begins at 7 AM with 60% efficiency by 9 AM.",
  },
  {
    icon: Sun,
    title: "Radiation-Production Correlation",
    description: "Solar radiation is the strongest predictor of energy output with a 0.94 correlation coefficient.",
    detail: "Every 100 W/m² increase in radiation corresponds to approximately 1.3 MW increase in production.",
  },
  {
    icon: Droplets,
    title: "Humidity Impact on Output",
    description: "High humidity (>75%) reduces solar panel efficiency by up to 15% due to atmospheric absorption.",
    detail: "Optimal humidity range: 30-50%. Morning dew evaporation delays peak efficiency by 30-45 minutes.",
  },
  {
    icon: TrendingUp,
    title: "Seasonal Production Patterns",
    description: "Summer months produce 40% more energy than winter due to longer daylight and higher solar angles.",
    detail: "Peak month: June (avg 72 MWh/day). Lowest month: December (avg 28 MWh/day).",
  },
  {
    icon: Battery,
    title: "Storage Optimization",
    description: "Battery charging should align with peak production windows for maximum efficiency.",
    detail: "Recommended charge window: 11 AM – 2 PM. This captures 65% of daily production in just 3 hours.",
  },
  {
    icon: BarChart3,
    title: "Wind Speed Effects",
    description: "Moderate wind (5-15 m/s) improves panel cooling and increases efficiency by 2-5%.",
    detail: "High winds (>25 m/s) trigger safety shutdowns. Optimal wind: 8-12 m/s for cooling benefit.",
  },
];

const InsightsSection = () => {
  return (
    <div className="mt-10">
      <h2 className="text-2xl font-display font-bold text-foreground mb-6">AI Insights</h2>
      <div className="grid md:grid-cols-2 gap-6">
        {insightsData.map((insight, i) => (
          <InsightCard key={insight.title} {...insight} index={i} />
        ))}
      </div>
    </div>
  );
};

export default InsightsSection;
