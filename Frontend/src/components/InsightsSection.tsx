import { motion } from "framer-motion";
import { TrendingUp, Droplets, Sun, Clock, Battery, BarChart3 } from "lucide-react";
import { Insight } from "@/lib/forecast-api";

interface InsightCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  detail: string;
  index: number;
}

type InsightsSectionProps = {
  insights: Insight[];
};

const iconMap: Record<string, React.ElementType> = {
  clock: Clock,
  sun: Sun,
  humidity: Droplets,
  trend: TrendingUp,
  battery: Battery,
  chart: BarChart3,
};

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

const InsightsSection = ({ insights }: InsightsSectionProps) => {
  return (
    <div className="mt-10">
      <h2 className="text-2xl font-display font-bold text-foreground mb-6">
        AI Insights
      </h2>

      <div className="grid md:grid-cols-2 gap-6">
        {insights.map((insight, i) => {
          const Icon =  Sun; // fallback icon

          return (
            <InsightCard
              key={i}
              icon={Icon}
              title={insight.title}
              description={insight.description}
              detail={insight.detail}
              index={i}
            />
          );
        })}
      </div>
    </div>
  );
};

export default InsightsSection;