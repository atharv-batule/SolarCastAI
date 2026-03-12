interface HeatmapPoint {
  date: string;
  hour: number;
  PredictedSolarPower: number;
}

interface RadiationHeatmapProps {
  data: HeatmapPoint[];
}

const RadiationHeatmap = ({ data }: RadiationHeatmapProps) => {
  const dates = Array.from(new Set(data.map(d => d.date))).sort();
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const valueMap = new Map<string, number>();
  data.forEach(d => {
    valueMap.set(`${d.date}-${d.hour}`, d.PredictedSolarPower);
  });

  const allValues = data.map(d => d.PredictedSolarPower);
  const maxVal = Math.max(...allValues, 0.0001);

  const getColor = (value: number) => {
    const ratio = value / maxVal;
    if (ratio > 0.8) return "bg-solar-yellow";
    if (ratio > 0.6) return "bg-solar-amber";
    if (ratio > 0.4) return "bg-solar-orange/70";
    if (ratio > 0.2) return "bg-solar-orange/40";
    if (ratio > 0.05) return "bg-solar-orange/20";
    return "bg-muted/50";
  };

  return (
    <div className="glass-card rounded-xl p-6">
      <h3 className="font-display font-semibold text-lg text-foreground mb-4">Production Heatmap</h3>
      <div className="overflow-x-auto">
        <div className="min-w-[600px]">
          <div className="flex gap-0.5 mb-1 pl-20">
            {hours.map((h) => (
              <div key={h} className="w-6 text-center text-[9px] text-muted-foreground">{h}</div>
            ))}
          </div>
          {dates.map((date) => (
            <div key={date} className="flex items-center gap-0.5 mb-0.5">
              <span className="w-20 text-[10px] text-muted-foreground text-right pr-2">{date.slice(5)}</span>
              {hours.map((h) => {
                const value = valueMap.get(`${date}-${h}`) ?? 0;
                return (
                  <div
                    key={h}
                    className={`w-6 h-5 rounded-sm ${getColor(value)} transition-colors`}
                    title={`${date} ${h}:00 - ${value.toFixed(2)} MW`}
                  />
                );
              })}
            </div>
          ))}
        </div>
      </div>
      <div className="flex items-center gap-3 mt-3 text-xs text-muted-foreground">
        <span>Low</span>
        <div className="flex gap-0.5">
          <span className="w-4 h-3 rounded-sm bg-muted/50" />
          <span className="w-4 h-3 rounded-sm bg-solar-orange/20" />
          <span className="w-4 h-3 rounded-sm bg-solar-orange/40" />
          <span className="w-4 h-3 rounded-sm bg-solar-orange/70" />
          <span className="w-4 h-3 rounded-sm bg-solar-amber" />
          <span className="w-4 h-3 rounded-sm bg-solar-yellow" />
        </div>
        <span>High</span>
      </div>
    </div>
  );
};

export default RadiationHeatmap;
