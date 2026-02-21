import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { workExperiences } from "@/data/skills";

const ExperiencePanel = () => {
  const [current, setCurrent] = useState(0);
  const exp = workExperiences[current];

  const prev = () => setCurrent(c => (c - 1 + workExperiences.length) % workExperiences.length);
  const next = () => setCurrent(c => (c + 1) % workExperiences.length);

  return (
    <div className="smw-panel p-2 h-full flex flex-col">
      <div className="border-b-2 border-smw-panel-border/30 pb-2 mb-2 flex items-center justify-between">
        <h2 className="font-pixel text-[7px] sm:text-[9px] text-primary smw-text-shadow">
          ⚙️ EXPERIÊNCIA
        </h2>
        <span className="font-pixel text-[5px] text-muted-foreground smw-text-shadow">
          {current + 1}/{workExperiences.length}
        </span>
      </div>

      <div className="flex-1 relative overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.25 }}
            className="flex flex-col gap-2"
          >
            <div className="flex items-center gap-2">
              <span className="text-xl">{exp.icon}</span>
              <div>
                <p className="font-pixel text-[6px] sm:text-[8px] text-primary smw-text-shadow">
                  {exp.company}
                </p>
                <p className="font-pixel text-[5px] sm:text-[6px] text-secondary smw-text-shadow">
                  {exp.role}
                </p>
              </div>
            </div>

            <p className="font-pixel text-[5px] text-smw-gold smw-text-shadow">
              📅 {exp.period}
            </p>

            <p className="font-pixel text-[4px] sm:text-[5px] text-foreground/80 smw-text-shadow leading-relaxed">
              {exp.description}
            </p>

            <div className="flex flex-wrap gap-1 mt-1">
              {exp.skills.map(skill => (
                <span
                  key={skill}
                  className="font-pixel text-[4px] sm:text-[5px] px-2 py-1 bg-smw-panel-border/20 border border-smw-panel-border/40 text-foreground smw-text-shadow"
                >
                  {skill}
                </span>
              ))}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation arrows */}
      <div className="flex items-center justify-between mt-2 pt-2 border-t-2 border-smw-panel-border/30">
        <button
          onClick={prev}
          className="font-pixel text-[8px] sm:text-[10px] text-primary hover:text-smw-gold transition-colors smw-text-shadow px-2"
        >
          ◀ PREV
        </button>
        <div className="flex gap-1">
          {workExperiences.map((_, i) => (
            <span
              key={i}
              className={`w-2 h-2 inline-block border border-smw-panel-border/50 ${
                i === current ? "bg-primary" : "bg-smw-xp-bg"
              }`}
            />
          ))}
        </div>
        <button
          onClick={next}
          className="font-pixel text-[8px] sm:text-[10px] text-primary hover:text-smw-gold transition-colors smw-text-shadow px-2"
        >
          NEXT ▶
        </button>
      </div>
    </div>
  );
};

export default ExperiencePanel;
