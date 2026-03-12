import { HourlyData } from "@/lib/types";


interface SolarTimelineProps {
  data: HourlyData[];
}

const getIntensityClass = (production: number, max: number) => {
  const ratio = production / max;
  if (ratio > 0.8) return "bg-solar-yellow";
  if (ratio > 0.5) return "bg-solar-amber";
  if (ratio > 0.2) return "bg-solar-orange/60";
  if (ratio > 0.05) return "bg-solar-orange/30";
  return "bg-muted";
};

const getIntensityLabel = (production: number, max: number) => {
  const ratio = production / max;
  if (ratio > 0.8) return "Peak";
  if (ratio > 0.5) return "High";
  if (ratio > 0.2) return "Medium";
  if (ratio > 0.05) return "Low";
  return "None";
};

const SolarTimeline = ({ data }: SolarTimelineProps) => {
  const maxProd = Math.max(...data.map(d => d.production));

  return (
    <div className="glass-card rounded-xl p-6">
      <h3 className="font-display font-semibold text-lg text-foreground mb-4">Solar Forecast Timeline</h3>
      <div className="flex gap-1 overflow-x-auto pb-2">
        {data.map((d) => (
          <div key={d.hour} className="flex flex-col items-center min-w-[40px]">
            <span className="text-[10px] text-muted-foreground mb-1">
              {getIntensityLabel(d.production, maxProd)}
            </span>
            <div
              className={`w-8 h-16 rounded-md ${getIntensityClass(d.production, maxProd)} transition-all`}
              title={`${d.production.toFixed(1)} MW`}
            />
            <span className="text-[10px] text-muted-foreground mt-1">{d.hour}h</span>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-4 mt-4 text-xs text-muted-foreground">
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-solar-yellow" /> Peak</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-solar-amber" /> High</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-solar-orange/60" /> Medium</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-muted" /> None</span>
      </div>
    </div>
  );
};

export default SolarTimeline;
