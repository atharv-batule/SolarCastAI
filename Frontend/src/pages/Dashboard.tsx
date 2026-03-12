import { Zap, Sun, Clock, Gauge } from "lucide-react";
import Navbar from "@/components/Navbar";
import MetricCard from "@/components/MetricCard";
import ProductionChart from "@/components/ProductionChart";
import SolarTimeline from "@/components/SolarTimeline";
import WeatherImpactChart from "@/components/WeatherImpactChart";
import RadiationHeatmap from "@/components/RadiationHeatmap";
import InsightPanel from "@/components/InsightPanel";
import SolarWindow from "@/components/SolarWindow";
import { useEffect, useState } from "react";
import { fetchSolarForecast } from "@/lib/forecast-api";
import { DailyForecast, HourlyData } from "@/lib/types";
//import { generateForecast, generateInsights } from "@/lib/mock-data";

function parseHour(dateHour: string) {
  return Number(dateHour.split(" ")[1].split(":")[0]);
}

const Dashboard = () => {
  const [forecast, setForecast] = useState<DailyForecast | null>(null);
const [loading, setLoading] = useState(true);

useEffect(() => {
  const run = async () => {
    try {
      const rows = await fetchSolarForecast();
      const today = new Date().toISOString().split("T")[0];
      const rowsForToday = rows.filter(r => r["Date-Hour"].startsWith(today));

      if (rowsForToday.length === 0) {
        setForecast(null);
        return;
      }

      const hourlyData: HourlyData[] = rowsForToday.map(r => ({
        hour: parseHour(r["Date-Hour"]),
        production: r["PredictedSolarPower"],
      }));

      const totalProduction = hourlyData.reduce((s, d) => s + d.production, 0);

      const peakEntry = hourlyData.reduce(
        (max, d) => (d.production > max.production ? d : max),
        hourlyData[0]
      );

      const sorted = [...hourlyData].sort((a, b) => b.production - a.production);
      const topHours = sorted.slice(0, 4).map(d => d.hour).sort((a, b) => a - b);
      const optimalStart = topHours[0];
      const optimalEnd = topHours[topHours.length - 1];
      const optimalProduction = hourlyData
        .filter(d => d.hour >= optimalStart && d.hour <= optimalEnd)
        .reduce((sum, d) => sum + d.production, 0);

      const solarPotentialScore = Math.round(
        Math.min(100, (totalProduction / 80) * 100)
      );

      setForecast({
        date: today,
        hourlyData,
        totalProduction,
        peakHour: peakEntry.hour,
        peakProduction: peakEntry.production,
        solarPotentialScore,
        optimalWindowStart: optimalStart,
        optimalWindowEnd: optimalEnd,
        optimalWindowProduction: optimalProduction,
      });
    } finally {
      setLoading(false);
    }
  };

  run();
}, []);

const latestProd =
  forecast?.hourlyData.find(d => d.hour === new Date().getHours())?.production ?? 0;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      {!loading && forecast && (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-display font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground mt-1">Real-time solar energy overview</p>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard title="Current Production" value={latestProd.toFixed(1)} unit="MW" icon={Zap} delay={0} />
          <MetricCard title="Predicted Daily Output" value={forecast.totalProduction.toFixed(1)} unit="MWh" icon={Sun} delay={0.1} />
          <MetricCard title="Peak Generation Hour" value={`${forecast.peakHour}:00`} icon={Clock} delay={0.2} />
          <MetricCard title="Solar Potential Score" value={forecast.solarPotentialScore} unit="/100" icon={Gauge} delay={0.3} />
        </div>

        {/* Solar Window */}
        <div className="mb-8">
          <SolarWindow
            startHour={forecast.optimalWindowStart}
            endHour={forecast.optimalWindowEnd}
            production={forecast.optimalWindowProduction}
          />
        </div>

        {/* Main Chart */}
        <div className="mb-8">
          <ProductionChart data={forecast.hourlyData} />
        </div>

        {/* Timeline */}
        <div className="mb-8">
          <SolarTimeline data={forecast.hourlyData} />
        </div>

        {/* Weather Impact + Insights */}
        {/* <div className="grid lg:grid-cols-2 gap-6 mb-8">
          <WeatherImpactChart data={forecast.hourlyData} />
          <InsightPanel insights={insights} />
        </div> */}

        {/* Heatmap */}
        <div className="mb-8">
          <RadiationHeatmap days={7} />
        </div>
      </div>
      )}
    </div>
  );
};

export default Dashboard;
