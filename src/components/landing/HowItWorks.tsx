import { Search, BarChart3, Target, Rocket, CheckCircle } from "lucide-react";

const steps = [
  {
    icon: Search,
    title: "Demand Proof Engine",
    description: "On scrappe les reviews G2 & Capterra d'outils SEO. Seuls les problèmes avec 10+ utilisateurs payants apparaissent.",
    detail: "Pas de bruit. Que des preuves de paiement.",
  },
  {
    icon: BarChart3,
    title: "Pain-to-Money Score",
    description: "Chaque problème reçoit un score 0–100 basé sur la fréquence, la frustration, et le budget déjà dépensé.",
    detail: "Score toujours accompagné de ses preuves.",
  },
  {
    icon: Target,
    title: "Market Gap Detector",
    description: "On identifie les failles des outils existants et un angle exploitable pour toi.",
    detail: "Pas d'angle clair → l'opportunité disparaît.",
  },
  {
    icon: Rocket,
    title: "Revenue Blueprint",
    description: "Pricing, client cible, canal d'acquisition, premier message d'outreach. Tout en 1 page.",
    detail: "Template prêt à exécuter en 48h.",
  },
  {
    icon: CheckCircle,
    title: "Build or Kill",
    description: "Lance un test 48h. Entre tes résultats. Verdict immédiat : CONTINUE, ITERATE ou KILL.",
    detail: "Fini les 3 mois perdus sur une mauvaise idée.",
  },
];

const HowItWorks = () => {
  return (
    <section className="py-24 relative">
      <div className="container px-6 max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-4">
            5 étapes. 30 minutes. <span className="text-gradient">Un verdict.</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-xl mx-auto">
            Chaque étape filtre brutalement. Ce qui reste est une opportunité réelle.
          </p>
        </div>

        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-8 top-0 bottom-0 w-px bg-border hidden md:block" />

          <div className="space-y-8">
            {steps.map((step, i) => (
              <div key={step.title} className="relative flex gap-6 md:gap-8 items-start group">
                {/* Icon */}
                <div className="relative z-10 flex-shrink-0 w-16 h-16 rounded-xl bg-surface border border-border flex items-center justify-center group-hover:border-primary/40 transition-colors duration-300">
                  <step.icon className="w-6 h-6 text-primary" />
                </div>

                {/* Content */}
                <div className="surface-card p-6 flex-1 group-hover:glow-border transition-all duration-300">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-xs font-mono text-primary">0{i + 1}</span>
                    <h3 className="text-lg font-semibold">{step.title}</h3>
                  </div>
                  <p className="text-muted-foreground mb-2">{step.description}</p>
                  <p className="text-sm text-primary font-medium">{step.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
