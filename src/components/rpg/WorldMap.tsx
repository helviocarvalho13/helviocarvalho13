import { useState } from "react";
import { regions, paths, ceoInfo } from "@/data/skills";
import type { Region } from "@/data/skills";
import MapRegion from "./MapRegion";
import PixelCharacter from "./PixelCharacter";
import SkillPanel from "./SkillPanel";

const WorldMap = () => {
  const [selectedRegion, setSelectedRegion] = useState<Region | null>(null);

  const handleSelect = (region: Region) => {
    setSelectedRegion(prev => (prev?.id === region.id ? null : region));
  };

  const getRegionPos = (id: string) => {
    const r = regions.find(r => r.id === id);
    return r ? r.position : { x: 50, y: 50 };
  };

  return (
    <div className="relative w-full min-h-screen">
      {/* Sky background */}
      <div className="relative w-full h-screen overflow-hidden">
        {/* Sky gradient */}
        <div
          className="absolute inset-0"
          style={{
            background: `linear-gradient(180deg, 
              hsl(210, 70%, 55%) 0%, 
              hsl(200, 60%, 65%) 40%, 
              hsl(190, 50%, 70%) 60%,
              hsl(135, 40%, 40%) 60.5%, 
              hsl(135, 45%, 35%) 100%)`
          }}
        />

        {/* Clouds */}
        <div className="absolute inset-0 pointer-events-none">
          {[
            { x: 8, y: 8, s: 1.2 }, { x: 30, y: 5, s: 0.8 }, { x: 55, y: 12, s: 1 },
            { x: 75, y: 6, s: 1.3 }, { x: 92, y: 10, s: 0.7 },
          ].map((c, i) => (
            <div
              key={i}
              className="absolute font-pixel text-foreground/80 smw-text-shadow select-none"
              style={{
                left: `${c.x}%`, top: `${c.y}%`,
                fontSize: `${c.s * 2}rem`,
              }}
            >
              ☁️
            </div>
          ))}
        </div>

        {/* Hills / terrain details */}
        <svg className="absolute inset-0 w-full h-full" viewBox="0 0 1000 600" preserveAspectRatio="none">
          {/* Terrain base */}
          <rect x="0" y="350" width="1000" height="250" fill="hsl(135, 45%, 32%)" />
          
          {/* Rolling hills */}
          <ellipse cx="150" cy="360" rx="200" ry="40" fill="hsl(135, 50%, 38%)" />
          <ellipse cx="500" cy="355" rx="250" ry="50" fill="hsl(130, 45%, 36%)" />
          <ellipse cx="800" cy="365" rx="180" ry="35" fill="hsl(140, 48%, 34%)" />
          
          {/* Mountain in background */}
          <polygon points="350,200 430,360 270,360" fill="hsl(30, 25%, 45%)" />
          <polygon points="350,200 390,280 310,280" fill="hsl(30, 20%, 55%)" />
          <polygon points="340,200 360,200 350,180" fill="hsl(0, 0%, 95%)" />

          {/* Water areas */}
          <ellipse cx="900" cy="520" rx="120" ry="60" fill="hsl(210, 70%, 50%)" opacity="0.7" />
          <ellipse cx="50" cy="540" rx="80" ry="40" fill="hsl(210, 70%, 50%)" opacity="0.5" />

          {/* Paths between nodes (SMW style dotted paths) */}
          {paths.map(([fromId, toId], i) => {
            const from = getRegionPos(fromId);
            const to = getRegionPos(toId);
            // Convert percentage to SVG coords
            const x1 = from.x * 10;
            const y1 = from.y * 6;
            const x2 = to.x * 10;
            const y2 = to.y * 6;
            return (
              <line
                key={i}
                x1={x1} y1={y1} x2={x2} y2={y2}
                stroke="hsl(40, 55%, 65%)"
                strokeWidth="6"
                strokeDasharray="12,10"
                strokeLinecap="round"
              />
            );
          })}

          {/* Path dots along lines */}
          {paths.map(([fromId, toId], i) => {
            const from = getRegionPos(fromId);
            const to = getRegionPos(toId);
            const dots = [];
            for (let t = 0.2; t <= 0.8; t += 0.2) {
              dots.push({
                cx: (from.x * 10) + (to.x * 10 - from.x * 10) * t,
                cy: (from.y * 6) + (to.y * 6 - from.y * 6) * t,
              });
            }
            return dots.map((d, j) => (
              <circle
                key={`${i}-${j}`}
                cx={d.cx} cy={d.cy} r="5"
                fill="hsl(48, 100%, 70%)"
                stroke="hsl(30, 50%, 35%)"
                strokeWidth="1.5"
              />
            ));
          })}

          {/* Decorative trees */}
          {[
            [60, 420], [180, 450], [320, 480], [450, 430], [580, 460],
            [700, 440], [820, 470], [250, 410], [650, 500], [130, 500],
            [400, 510], [530, 380], [760, 390], [880, 410],
          ].map(([x, y], i) => (
            <text key={`tree-${i}`} x={x} y={y} fontSize="28" textAnchor="middle">
              🌲
            </text>
          ))}

          {/* Bushes */}
          {[
            [100, 470], [300, 440], [500, 490], [680, 460], [850, 500],
          ].map(([x, y], i) => (
            <text key={`bush-${i}`} x={x} y={y} fontSize="18" textAnchor="middle">
              🌿
            </text>
          ))}
        </svg>

        {/* Region nodes */}
        {regions.map(region => (
          <MapRegion
            key={region.id}
            region={region}
            isSelected={selectedRegion?.id === region.id}
            onSelect={handleSelect}
          />
        ))}

        {/* Character */}
        <PixelCharacter
          targetRegion={selectedRegion}
          defaultPosition={{ x: 12, y: 48 }}
        />

        {/* CEO Info Banner (bottom of map, SMW style) */}
        <div className="absolute bottom-4 left-4 right-4 sm:left-auto sm:right-4 sm:bottom-4 sm:w-80 z-30">
          <div className="smw-panel p-3">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 flex items-center justify-center text-2xl border-2 border-smw-panel-border bg-smw-panel-bg">
                🎮
              </div>
              <div>
                <p className="font-pixel text-[8px] sm:text-[9px] text-primary smw-text-shadow">
                  {ceoInfo.name}
                </p>
                <p className="font-pixel text-[6px] text-muted-foreground smw-text-shadow">
                  {ceoInfo.title}
                </p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2 mt-2">
              <div className="text-center">
                <p className="font-pixel text-[10px] text-primary smw-text-shadow">{ceoInfo.yearsOfExp}</p>
                <p className="font-pixel text-[5px] text-muted-foreground">ANOS EXP</p>
              </div>
              <div className="text-center">
                <p className="font-pixel text-[10px] text-primary smw-text-shadow">{ceoInfo.completedQuests}</p>
                <p className="font-pixel text-[5px] text-muted-foreground">PROJETOS</p>
              </div>
              <div className="text-center">
                <p className="font-pixel text-[10px] text-primary smw-text-shadow">{ceoInfo.worldsExplored}</p>
                <p className="font-pixel text-[5px] text-muted-foreground">MUNDOS</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Skill Panel */}
      <SkillPanel region={selectedRegion} onClose={() => setSelectedRegion(null)} />
    </div>
  );
};

export default WorldMap;
