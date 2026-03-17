import { useState } from "react";
import { CalendarIcon, Loader2, Zap, Sun, Clock, Gauge } from "lucide-react";
import Navbar from "@/components/Navbar";
import MetricCard from "@/components/MetricCard";
import ProductionChart from "@/components/ProductionChart";
import SolarWindow from "@/components/SolarWindow";
import InsightsSection from "@/components/InsightsSection";
import { fetchSolarForecast, Insight } from "@/lib/forecast-api";
import { fetchAnalytics } from "@/lib/analytics-api";

type HourlyData = {
  hour: number;
  production: number;
};

type DailyForecast = {
  date: string;
  hourlyData: HourlyData[];
  totalProduction: number;
  peakHour: number;
  peakProduction: number;
  solarPotentialScore: number;
  optimalWindowStart: number;
  optimalWindowEnd: number;
  optimalWindowProduction: number;
};

const ForecastPage = () => {
  const [selectedDate, setSelectedDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DailyForecast | null>(null);
  const [insights, setInsights] = useState<Insight[]>([]); // ✅ NEW

  const handlePredict = async () => {
    if (!selectedDate) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetchSolarForecast();

      const rows = response.forecast;
      const insightsData = response.insights || []; // ✅ NEW

      setInsights(insightsData); // ✅ NEW

      const selected = new Date(selectedDate);

      const rowsForDate = rows.filter((r) => {
        const date = new Date(r["Date-Hour"]);
        return (
          date.getFullYear() === selected.getFullYear() &&
          date.getMonth() === selected.getMonth() &&
          date.getDate() === selected.getDate()
        );
      });

      if (rowsForDate.length === 0) {
        setResult(null);
        return;
      }

      const hourlyData: HourlyData[] = rowsForDate.map((r) => ({
        hour: new Date(r["Date-Hour"]).getHours(),
        production: r["PredictedSolarPower"],
      }));

      const totalProduction = hourlyData.reduce(
        (s, d) => s + d.production,
        0
      );

      const analytics = await fetchAnalytics();

      const avgDailyProduction =
        analytics.solar_production_trends.length > 0
          ? analytics.solar_production_trends.reduce(
              (s, d) => s + d.PredictedSolarPower,
              0
            ) / analytics.solar_production_trends.length
          : null;

      const peakEntry = hourlyData.reduce(
        (max, d) => (d.production > max.production ? d : max),
        hourlyData[0]
      );

      const sorted = [...hourlyData].sort(
        (a, b) => b.production - a.production
      );

      const topHours = sorted
        .slice(0, 4)
        .map((d) => d.hour)
        .sort((a, b) => a - b);

      const optimalStart = topHours[0];
      const optimalEnd = topHours[topHours.length - 1];

      const optimalProduction = hourlyData
        .filter((d) => d.hour >= optimalStart && d.hour <= optimalEnd)
        .reduce((sum, d) => sum + d.production, 0);

      const solarPotentialScore =
        avgDailyProduction && avgDailyProduction > 0
          ? Math.round(
              Math.min(100, (totalProduction / avgDailyProduction) * 100)
            )
          : 0;

      setResult({
        date: selectedDate,
        hourlyData,
        totalProduction,
        peakHour: peakEntry.hour,
        peakProduction: peakEntry.production,
        solarPotentialScore,
        optimalWindowStart: optimalStart,
        optimalWindowEnd: optimalEnd,
        optimalWindowProduction: optimalProduction,
      });
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-2">Solar Forecast</h1>

        {/* Input */}
        <div className="p-4 border rounded mb-6">
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="border p-2 mr-2"
          />

          <button onClick={handlePredict} className="bg-yellow-500 px-4 py-2 text-white">
            {loading ? "Loading..." : "Predict"}
          </button>
        </div>

        {/* Results */}
        {result && (
          <>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <MetricCard title="Total Output" value={result.totalProduction.toFixed(1)} unit="MWh" icon={Sun} delay={0} />
              <MetricCard title="Peak Hour" value={`${result.peakHour}:00`} icon={Clock} delay={0.1} />
              <MetricCard title="Peak Power" value={result.peakProduction.toFixed(1)} unit="MW" icon={Zap} delay={0.2} />
              <MetricCard title="Score" value={result.solarPotentialScore} unit="/100" icon={Gauge} delay={0.3} />
            </div>

            <SolarWindow
              startHour={result.optimalWindowStart}
              endHour={result.optimalWindowEnd}
              production={result.optimalWindowProduction}
            />

            <ProductionChart data={result.hourlyData} />

            {/* ✅ DYNAMIC INSIGHTS */}
            <div className="mt-6">
              <InsightsSection insights={insights} />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ForecastPage;