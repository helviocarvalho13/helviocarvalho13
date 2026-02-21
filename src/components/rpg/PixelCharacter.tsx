import { motion } from "framer-motion";
import type { Region } from "@/data/skills";

interface PixelCharacterProps {
  targetRegion: Region | null;
  defaultPosition: { x: number; y: number };
}

const PixelCharacter = ({ targetRegion, defaultPosition }: PixelCharacterProps) => {
  const pos = targetRegion
    ? { x: targetRegion.position.x, y: targetRegion.position.y - 7 }
    : defaultPosition;

  return (
    <motion.div
      className="absolute z-20 pointer-events-none"
      animate={{
        left: `${pos.x}%`,
        top: `${pos.y}%`,
      }}
      transition={{ type: "spring", damping: 14, stiffness: 80 }}
      style={{ transform: "translate(-50%, -50%)" }}
    >
      {/* Mario-style character */}
      <div className={`text-3xl sm:text-4xl ${targetRegion ? "animate-walk" : "animate-float"}`}>
        🧑‍💻
      </div>
      {/* Shadow */}
      <div className="w-5 h-1.5 bg-foreground/20 rounded-full mx-auto -mt-1" />
    </motion.div>
  );
};

export default PixelCharacter;
