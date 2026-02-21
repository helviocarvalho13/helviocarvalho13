import { motion } from "framer-motion";
import type { Region } from "@/data/skills";

interface MapRegionProps {
  region: Region;
  isSelected: boolean;
  onSelect: (region: Region) => void;
}

const nodeIcons: Record<string, string> = {
  normal: "●",
  castle: "🏰",
  fortress: "⛰️",
  ghost: "🌲",
  star: "⭐",
};

const MapRegion = ({ region, isSelected, onSelect }: MapRegionProps) => {
  return (
    <motion.button
      className="absolute group cursor-pointer focus:outline-none z-10"
      style={{
        left: `${region.position.x}%`,
        top: `${region.position.y}%`,
        transform: "translate(-50%, -50%)",
      }}
      onClick={() => onSelect(region)}
      whileHover={{ scale: 1.2 }}
      whileTap={{ scale: 0.9 }}
    >
      {/* Node circle (SMW style) */}
      <div
        className={`smw-node flex items-center justify-center text-xl sm:text-2xl transition-all duration-200 ${
          isSelected ? "smw-node-selected animate-bounce-node" : ""
        }`}
        style={{ width: "48px", height: "48px" }}
      >
        <span className={isSelected ? "animate-star-spin" : ""}>
          {nodeIcons[region.nodeType] || "●"}
        </span>
      </div>

      {/* Region name label */}
      <div
        className={`absolute -bottom-7 left-1/2 -translate-x-1/2 whitespace-nowrap font-pixel text-[6px] sm:text-[7px] smw-text-shadow transition-colors duration-200 ${
          isSelected ? "text-primary" : "text-foreground/80"
        }`}
      >
        {region.name}
      </div>

      {/* Skill count badge */}
      <div className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-smw-red flex items-center justify-center border border-foreground/30">
        <span className="font-pixel text-[5px] text-foreground smw-text-shadow">
          {region.skills.length}
        </span>
      </div>

      {/* Hover tooltip */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        whileHover={{ opacity: 1, y: 0 }}
        className="absolute -top-14 left-1/2 -translate-x-1/2 smw-panel p-2 z-30 min-w-[110px] pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity"
      >
        <p className="text-primary font-pixel text-[6px] text-center smw-text-shadow">
          {region.emoji} {region.name}
        </p>
        <p className="text-muted-foreground font-pixel text-[5px] text-center mt-1">
          {region.skills.length} skills → Clique!
        </p>
      </motion.div>
    </motion.button>
  );
};

export default MapRegion;
