import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Starter",
    price: "49",
    description: "Pour tester tes premières opportunités",
    features: [
      "10 opportunités / mois",
      "5 tests 48h",
      "Pain-to-Money Score",
      "Market Gap Detector",
      "Revenue Blueprint",
    ],
    cta: "Rejoindre la waitlist",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "99",
    description: "Pour valider sérieusement, chaque mois",
    features: [
      "30 opportunités / mois",
      "Tests illimités",
      "Tout Starter inclus",
      "Export des rapports",
      "Dashboard personnel",
    ],
    cta: "Rejoindre la waitlist",
    highlighted: true,
  },
  {
    name: "Elite",
    price: "149",
    description: "Accompagnement personnalisé",
    features: [
      "Tout Pro inclus",
      "Appel mensuel review",
      "Opportunités prioritaires",
      "Support dédié",
      "Accès anticipé nouvelles features",
    ],
    cta: "Rejoindre la waitlist",
    highlighted: false,
  },
];

const Pricing = () => {
  return (
    <section className="py-24 relative">
      <div className="container px-6 max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-4">
            Un prix. <span className="text-gradient">Pas de freemium.</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-xl mx-auto">
            Le freemium attire les curieux. On veut des freelances prêts à agir.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`surface-card p-8 flex flex-col relative ${
                plan.highlighted ? "glow-border border-primary/30" : ""
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  Populaire
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-1">{plan.name}</h3>
                <p className="text-sm text-muted-foreground">{plan.description}</p>
              </div>

              <div className="flex items-baseline gap-1 mb-8">
                <span className="text-4xl font-black">{plan.price}€</span>
                <span className="text-muted-foreground text-sm">/mois</span>
              </div>

              <ul className="space-y-3 mb-8 flex-1">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3 text-sm">
                    <Check className="w-4 h-4 text-primary flex-shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                variant={plan.highlighted ? "hero" : "hero-outline"}
                className="w-full"
              >
                {plan.cta}
              </Button>
            </div>
          ))}
        </div>

        <p className="text-center text-sm text-muted-foreground mt-8">
          Essai 7 jours à 1€ · Annulation en 1 clic · validation ≠ revenu garanti
        </p>
      </div>
    </section>
  );
};

export default Pricing;
