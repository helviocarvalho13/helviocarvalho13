import { useState } from "react";
import { motion } from "framer-motion";
import { regions, ceoInfo, totalXP, maxXP } from "@/data/skills";
import type { Region } from "@/data/skills";
import MenuSidebar from "./MenuSidebar";
import InventoryPanel from "./InventoryPanel";
import LevelsPanel from "./LevelsPanel";
import ExperiencePanel from "./ExperiencePanel";
import VolunteerPanel from "./VolunteerPanel";

const RPGMenuLayout = () => {
  const [selectedRegion, setSelectedRegion] = useState<Region | null>(null);
  const level = Math.floor(totalXP / 15);
  const xpPercent = Math.round((totalXP / maxXP) * 100);

  return (
    <div
      className="min-h-screen relative overflow-hidden flex flex-col"
      style={{
        background: `linear-gradient(180deg, 
          hsl(210, 70%, 55%) 0%, 
          hsl(200, 60%, 65%) 30%, 
          hsl(135, 40%, 40%) 55%, 
          hsl(135, 45%, 30%) 100%)`,
      }}
    >
      {/* Decorative scenery (behind panels) */}
      <div className="absolute inset-0 pointer-events-none select-none">
        {/* Clouds */}
        {[
          { x: 5, y: 4, s: 1.3 }, { x: 25, y: 8, s: 0.9 }, { x: 50, y: 3, s: 1.1 },
          { x: 72, y: 7, s: 1.4 }, { x: 90, y: 5, s: 0.8 },
        ].map((c, i) => (
          <div
            key={i}
            className="absolute text-foreground/70 animate-float"
            style={{ left: `${c.x}%`, top: `${c.y}%`, fontSize: `${c.s * 2}rem`, animationDelay: `${i * 0.6}s` }}
          >
            ☁️
          </div>
        ))}
        {/* Trees */}
        {[
          [8, 70], [20, 75], [35, 68], [55, 72], [70, 78], [85, 70], [95, 76],
          [15, 85], [40, 88], [60, 82], [80, 86],
        ].map(([x, y], i) => (
          <div key={`tree-${i}`} className="absolute text-lg sm:text-2xl" style={{ left: `${x}%`, top: `${y}%` }}>
            🌲
          </div>
        ))}
        {/* Character in scene */}
        <div className="absolute animate-float" style={{ left: "48%", top: "60%", animationDelay: "1s" }}>
          <span className="text-3xl sm:text-4xl">🧙</span>
        </div>
        {/* Small house */}
        <div className="absolute" style={{ left: "42%", top: "55%" }}>
          <span className="text-2xl sm:text-3xl">🏠</span>
        </div>
      </div>

      {/* HUD Header */}
      <header className="relative z-20 smw-panel p-2 sm:p-3 mx-2 mt-2 sm:mx-4 sm:mt-3">
        <div className="flex items-center justify-between gap-2 text-[7px] sm:text-[9px]">
          <div className="flex items-center gap-2">
            <span className="text-lg">🎮</span>
            <div>
              <p className="text-primary smw-text-shadow font-pixel">{ceoInfo.name}</p>
              <p className="text-muted-foreground font-pixel text-[5px] sm:text-[6px]">
                {ceoInfo.title} — {ceoInfo.company}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm animate-star-spin">⭐</span>
            <span className="text-primary smw-text-shadow font-pixel">×{totalXP}</span>
          </div>
          <div className="text-center">
            <p className="text-primary smw-text-shadow font-pixel">LV.{level}</p>
            <div className="flex items-center gap-1 mt-0.5">
              <div className="w-16 sm:w-24 h-2.5 bg-smw-xp-bg border border-smw-panel-border relative overflow-hidden">
                <div className="h-full bg-smw-xp-bar transition-all duration-1000 relative" style={{ width: `${xpPercent}%` }}>
                  <div className="absolute inset-0 xp-bar-shimmer" />
                </div>
              </div>
              <span className="text-muted-foreground font-pixel text-[5px]">{xpPercent}%</span>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-3">
            <a href={ceoInfo.linkedin} target="_blank" rel="noopener noreferrer" className="font-pixel text-[6px] text-secondary hover:text-primary transition-colors smw-text-shadow">
              LinkedIn
            </a>
            <a href={ceoInfo.github} target="_blank" rel="noopener noreferrer" className="font-pixel text-[6px] text-secondary hover:text-primary transition-colors smw-text-shadow">
              GitHub
            </a>
            <a href={ceoInfo.companyUrl} target="_blank" rel="noopener noreferrer" className="font-pixel text-[6px] text-secondary hover:text-primary transition-colors smw-text-shadow">
              Luna Tech
            </a>
          </div>
        </div>
      </header>

      {/* Main content grid */}
      <main className="relative z-10 flex-1 p-2 sm:p-4 grid grid-cols-1 lg:grid-cols-[200px_1fr_280px] gap-3 sm:gap-4 min-h-0">
        {/* Left sidebar - Skill categories */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4 }}
          className="lg:self-start"
        >
          <MenuSidebar
            regions={regions}
            selectedRegion={selectedRegion}
            onSelectRegion={setSelectedRegion}
          />

          {/* Player stats below sidebar */}
          <div className="smw-panel p-2 mt-3">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-lg">🧙</span>
              <div>
                <p className="font-pixel text-[6px] sm:text-[7px] text-primary smw-text-shadow">STATS</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-1">
              <div className="text-center">
                <p className="font-pixel text-[8px] sm:text-[10px] text-primary smw-text-shadow">{ceoInfo.yearsOfExp}</p>
                <p className="font-pixel text-[4px] text-muted-foreground">ANOS</p>
              </div>
              <div className="text-center">
                <p className="font-pixel text-[8px] sm:text-[10px] text-primary smw-text-shadow">{ceoInfo.completedQuests}</p>
                <p className="font-pixel text-[4px] text-muted-foreground">QUESTS</p>
              </div>
              <div className="text-center">
                <p className="font-pixel text-[8px] sm:text-[10px] text-primary smw-text-shadow">{ceoInfo.worldsExplored}</p>
                <p className="font-pixel text-[4px] text-muted-foreground">MUNDOS</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Center - Inventory (skills grid) + Experience carousel */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="flex flex-col gap-3 sm:gap-4 min-h-0"
        >
          <div className="flex-1 min-h-[250px]">
            <InventoryPanel region={selectedRegion} />
          </div>
          <div className="min-h-[180px]">
            <ExperiencePanel />
          </div>
        </motion.div>

        {/* Right side - Levels + Volunteer */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="flex flex-col gap-3 sm:gap-4 min-h-0"
        >
          <div className="flex-1 min-h-[250px]">
            <LevelsPanel />
          </div>
          <div className="min-h-[180px]">
            <VolunteerPanel />
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default RPGMenuLayout;
